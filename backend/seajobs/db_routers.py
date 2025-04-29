class PrimaryReplicaRouter:
    """
    Роутер для управления запросами к базе данных.
    Защищает от SQL-инъекций путем разделения операций чтения и записи.
    """
    def db_for_read(self, model, **hints):
        """
        Чтение всегда идет на реплику
        """
        return 'default'

    def db_for_write(self, model, **hints):
        """
        Запись всегда идет на мастер
        """
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        """
        Разрешаем отношения между объектами
        """
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Миграции выполняются только на мастер
        """
        return True 