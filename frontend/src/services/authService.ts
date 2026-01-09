import apiClient from './api';
import { LoginRequest, RegisterRequest, AuthResponse, UserProfile } from '../types';

export const authService = {
  // Login
  async login(credentials: LoginRequest): Promise<AuthResponse> {
    const response = await apiClient.post<AuthResponse>('/api/auth/login', credentials);
    
    // Store tokens
    localStorage.setItem('access_token', response.access_token);
    localStorage.setItem('refresh_token', response.refresh_token);
    
    // Fetch and store user profile
    const profile = await this.getCurrentUser();
    localStorage.setItem('user', JSON.stringify(profile));
    
    return response;
  },

  // Register
  async register(userData: RegisterRequest): Promise<AuthResponse> {
    const response = await apiClient.post<AuthResponse>('/api/auth/register', userData);
    
    // Store tokens
    localStorage.setItem('access_token', response.access_token);
    localStorage.setItem('refresh_token', response.refresh_token);
    
    // Fetch and store user profile
    const profile = await this.getCurrentUser();
    localStorage.setItem('user', JSON.stringify(profile));
    
    return response;
  },

  // Get current user profile
  async getCurrentUser(): Promise<UserProfile> {
    return await apiClient.get<UserProfile>('/api/auth/me');
  },

  // Logout
  logout(): void {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user');
  },

  // Check if user is authenticated
  isAuthenticated(): boolean {
    return !!localStorage.getItem('access_token');
  },

  // Get stored user
  getStoredUser(): UserProfile | null {
    const userStr = localStorage.getItem('user');
    return userStr ? JSON.parse(userStr) : null;
  },

  // Get user role
  getUserRole(): string | null {
    const user = this.getStoredUser();
    return user?.user.role || null;
  },
};