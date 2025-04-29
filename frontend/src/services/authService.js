import axios from 'axios';

// Create an axios instance with a base URL
const API_URL = '/api';

// Create an axios instance
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add authorization header for authenticated requests
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Login user and get tokens
export const loginUser = async (email, password) => {
  const response = await api.post('/auth/login/', { email, password });
  return response.data;
};

// Register a new user
export const registerUser = async (userData) => {
  const response = await api.post('/auth/register/', userData);
  return response.data;
};

// Refresh access token
export const refreshToken = async (refreshToken) => {
  const response = await api.post('/auth/token/refresh/', { refresh: refreshToken });
  return response.data;
};

// Get current user profile
export const fetchCurrentUser = async () => {
  const response = await api.get('/users/me/');
  return response.data;
};

// Update user profile
export const updateUserProfile = async (profileData) => {
  const response = await api.put('/users/me/', profileData);
  return response.data;
};

// Request password reset
export const requestPasswordReset = async (email) => {
  const response = await api.post('/auth/password-reset/', { email });
  return response.data;
};

// Confirm password reset
export const confirmPasswordReset = async (uid, token, newPassword1, newPassword2) => {
  const response = await api.post('/auth/password-reset/confirm/', {
    uid,
    token,
    new_password1: newPassword1,
    new_password2: newPassword2
  });
  return response.data;
};

// Export the API instance for use in other services
export default api;