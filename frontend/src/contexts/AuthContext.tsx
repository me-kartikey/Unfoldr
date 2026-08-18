import React, { createContext, useContext, useState, useEffect } from "react";
import api from "@/api/axios";

// Created on 13-08-2026: AuthContext providing session authentication states, registration, login, and automatic resume from HttpOnly cookies.

interface User {
  id: string;
  email: string;
  username: string;
  role: string;
  is_active: boolean;
}

interface AuthContextType {
  user: User | null;
  loading: boolean;
  login: (usernameOrEmail: string, password: string) => Promise<void>;
  register: (email: string, username: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  // Resume user session on mount
  const checkAuth = async () => {
    try {
      const response = await api.get("/auth/me");
      setUser(response.data);
    } catch (error) {
      setUser(null);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    checkAuth();

    // Listen for global 401 unauthorized interceptor events to clear state
    const handleUnauthorized = () => {
      setUser(null);
    };

    window.addEventListener("unauthorized", handleUnauthorized);
    return () => {
      window.removeEventListener("unauthorized", handleUnauthorized);
    };
  }, []);

  const login = async (usernameOrEmail: string, password: string) => {
    setLoading(true);
    try {
      await api.post("/auth/login", {
        username_or_email: usernameOrEmail,
        password: password,
      });
      // Fetch user profile after successful login sets the cookie
      const response = await api.get("/auth/me");
      setUser(response.data);
    } catch (error: any) {
      setUser(null);
      throw error;
    } finally {
      setLoading(false);
    }
  };

  const register = async (email: string, username: string, password: string) => {
    setLoading(true);
    try {
      await api.post("/auth/register", {
        email,
        username,
        password,
      });
    } finally {
      setLoading(false);
    }
  };

  const logout = async () => {
    setLoading(true);
    try {
      await api.post("/auth/logout");
    } finally {
      setUser(null);
      setLoading(false);
    }
  };

  return (
    <AuthContext.Provider value={{ user, loading, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
};
