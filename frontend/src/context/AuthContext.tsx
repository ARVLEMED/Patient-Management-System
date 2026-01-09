import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { UserProfile, LoginRequest, RegisterRequest } from '../types';
import { authService } from '../services/authService';

interface AuthContextType {
  user: UserProfile | null;
  loading: boolean;
  login: (credentials: LoginRequest) => Promise<void>;
  register: (userData: RegisterRequest) => Promise<void>;
  logout: () => void;
  isAuthenticated: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<UserProfile | null>(null);
  const [loading, setLoading] = useState(true);

  // Load user from localStorage on mount
  useEffect(() => {
  const storedUser = authService.getStoredUser();

  if (storedUser && storedUser.user && storedUser.user.role) {
    setUser(storedUser);
  } else {
    setUser(null);
  }

  setLoading(false);
}, []);
const login = async (credentials: LoginRequest) => {
  await authService.login(credentials);

  const userProfile = authService.getStoredUser();

  if (!userProfile || !userProfile.user?.role) {
    throw new Error('Invalid user profile returned from login');
  }

  setUser(userProfile);
};


  const register = async (userData: RegisterRequest) => {
  await authService.register(userData);

  const userProfile = authService.getStoredUser();

  if (!userProfile || !userProfile.user?.role) {
    throw new Error('Invalid user profile returned from registration');
  }

  setUser(userProfile);
};


  const logout = () => {
    authService.logout();
    setUser(null);
  };

  const value = {
  user,
  loading,
  login,
  register,
  logout,
  isAuthenticated: !!user?.user?.role,
};


  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};