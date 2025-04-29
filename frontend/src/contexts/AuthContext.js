import React, { createContext, useContext, useState, useEffect } from 'react';
import jwt_decode from 'jwt-decode';
import { useNavigate } from 'react-router-dom';
import { loginUser, registerUser, refreshToken, fetchCurrentUser } from '../services/authService';

// Create the context
const AuthContext = createContext(null);

// Custom hook to use the auth context
export const useAuth = () => useContext(AuthContext);

export const AuthProvider = ({ children }) => {
  // State
  const [currentUser, setCurrentUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem('access_token'));
  const [refreshTokenValue, setRefreshTokenValue] = useState(localStorage.getItem('refresh_token'));
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  const navigate = useNavigate();

  // Check if token is valid or expired
  const isTokenValid = () => {
    if (!token) return false;
    
    try {
      const decoded = jwt_decode(token);
      const currentTime = Date.now() / 1000;
      
      // Check if token is not expired
      return decoded.exp > currentTime;
    } catch (error) {
      console.error('Token validation error:', error);
      return false;
    }
  };

  // Computed value for authentication status
  const isAuthenticated = !!token && isTokenValid();

  // Load user profile if authenticated
  useEffect(() => {
    const loadUserProfile = async () => {
      if (isAuthenticated && !currentUser) {
        try {
          setLoading(true);
          const userData = await fetchCurrentUser();
          setCurrentUser(userData);
          setError(null);
        } catch (err) {
          console.error('Error loading user profile:', err);
          setError('Failed to load user profile');
          logout();
        } finally {
          setLoading(false);
        }
      } else {
        setLoading(false);
      }
    };

    loadUserProfile();
  }, [token]);

  // Refresh token when it's about to expire
  useEffect(() => {
    if (isAuthenticated) {
      const decoded = jwt_decode(token);
      const currentTime = Date.now() / 1000;
      
      // If token is about to expire in the next 5 minutes, refresh it
      if (decoded.exp - currentTime < 300) {
        handleRefreshToken();
      }
      
      // Set up timer to refresh token
      const timeToExpiry = (decoded.exp - currentTime) * 1000 - 5 * 60 * 1000; // 5 minutes before expiry
      const refreshTimer = setTimeout(handleRefreshToken, timeToExpiry > 0 ? timeToExpiry : 0);
      
      return () => clearTimeout(refreshTimer);
    }
  }, [token, refreshTokenValue]);

  // Login function
  const login = async (email, password) => {
    try {
      setLoading(true);
      setError(null);
      
      const authData = await loginUser(email, password);
      
      // Store tokens in localStorage
      localStorage.setItem('access_token', authData.access);
      localStorage.setItem('refresh_token', authData.refresh);
      
      // Update state
      setToken(authData.access);
      setRefreshTokenValue(authData.refresh);
      setCurrentUser(authData.user);
      
      return authData;
    } catch (err) {
      console.error('Login error:', err);
      setError(err.response?.data?.detail || 'Login failed');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  // Register function
  const register = async (userData) => {
    try {
      setLoading(true);
      setError(null);
      
      const response = await registerUser(userData);
      
      // Login after successful registration
      if (response.user) {
        await login(userData.email, userData.password1);
      }
      
      return response;
    } catch (err) {
      console.error('Registration error:', err);
      setError(err.response?.data || 'Registration failed');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  // Refresh token function
  const handleRefreshToken = async () => {
    if (!refreshTokenValue) return;
    
    try {
      const newTokens = await refreshToken(refreshTokenValue);
      
      // Update tokens
      localStorage.setItem('access_token', newTokens.access);
      if (newTokens.refresh) {
        localStorage.setItem('refresh_token', newTokens.refresh);
        setRefreshTokenValue(newTokens.refresh);
      }
      
      setToken(newTokens.access);
      setError(null);
    } catch (err) {
      console.error('Token refresh error:', err);
      setError('Session expired. Please login again.');
      logout();
    }
  };

  // Logout function
  const logout = () => {
    // Clear tokens from localStorage
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    
    // Update state
    setToken(null);
    setRefreshTokenValue(null);
    setCurrentUser(null);
    
    // Redirect to login page
    navigate('/login');
  };

  // Value provided by the context
  const value = {
    currentUser,
    isAuthenticated,
    loading,
    error,
    login,
    logout,
    register,
    handleRefreshToken
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};