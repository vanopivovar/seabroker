from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Conversation, Message, Notification, EmailSubscription
from apps.accounts.serializers import UserSerializer

User = get_user_model()

class MessageSerializer(serializers.ModelSerializer):
    """Serializer for messages"""
    sender = UserSerializer(read_only=True)
    
    class Meta:
        model = Message
        fields = '__all__'
        read_only_fields = ['id', 'conversation', 'sender', 'is_read', 'read_at', 'created_at']

class ConversationListSerializer(serializers.ModelSerializer):
    """Serializer for conversation list view"""
    participants = UserSerializer(many=True, read_only=True)
    last_message = serializers.SerializerMethodField()
    unread_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Conversation
        fields = ['id', 'participants', 'last_message', 'unread_count', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_last_message(self, obj):
        """Get the last message in the conversation"""
        last_message = obj.messages.order_by('-created_at').first()
        if last_message:
            return {
                'id': last_message.id,
                'content': last_message.content[:100],  # Preview only
                'sender': last_message.sender.email,
                'created_at': last_message.created_at
            }
        return None
    
    def get_unread_count(self, obj):
        """Get the count of unread messages for the current user"""
        user = self.context['request'].user
        return obj.messages.filter(is_read=False).exclude(sender=user).count()

class ConversationDetailSerializer(serializers.ModelSerializer):
    """Serializer for conversation detail view"""
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)
    
    class Meta:
        model = Conversation
        fields = ['id', 'participants', 'messages', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class ConversationCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating a new conversation"""
    participant_ids = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        many=True,
        write_only=True
    )
    initial_message = serializers.CharField(write_only=True)
    
    class Meta:
        model = Conversation
        fields = ['participant_ids', 'initial_message']
    
    def validate_participant_ids(self, participant_ids):
        """Validate participant IDs"""
        user = self.context['request'].user
        
        # Ensure current user is not in the participants list
        if user in participant_ids:
            raise serializers.ValidationError("You cannot include yourself in the participants list")
        
        # Ensure there's at least one participant
        if not participant_ids:
            raise serializers.ValidationError("You must include at least one participant")
        
        return participant_ids
    
    def create(self, validated_data):
        """Create a new conversation with an initial message"""
        participant_ids = validated_data.pop('participant_ids')
        initial_message = validated_data.pop('initial_message')
        user = self.context['request'].user
        
        # Create the conversation
        conversation = Conversation.objects.create(**validated_data)
        
        # Add participants including the current user
        conversation.participants.add(user, *participant_ids)
        
        # Create the initial message
        Message.objects.create(
            conversation=conversation,
            sender=user,
            content=initial_message
        )
        
        return conversation

class MessageCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating a new message"""
    class Meta:
        model = Message
        fields = ['content', 'attachment']
    
    def create(self, validated_data):
        """Create a new message"""
        conversation = self.context['conversation']
        user = self.context['request'].user
        
        # Ensure user is a participant in the conversation
        if not conversation.participants.filter(id=user.id).exists():
            raise serializers.ValidationError("You are not a participant in this conversation")
        
        # Create the message
        message = Message.objects.create(
            conversation=conversation,
            sender=user,
            **validated_data
        )
        
        # Update conversation last modified time
        conversation.updated_at = message.created_at
        conversation.save(update_fields=['updated_at'])
        
        return message

class NotificationSerializer(serializers.ModelSerializer):
    """Serializer for notifications"""
    class Meta:
        model = Notification
        fields = '__all__'
        read_only_fields = ['id', 'recipient', 'notification_type', 'title', 'message', 
                           'related_object_id', 'related_object_type', 'created_at']

class EmailSubscriptionSerializer(serializers.ModelSerializer):
    """Serializer for email subscription preferences"""
    class Meta:
        model = EmailSubscription
        fields = '__all__'
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']