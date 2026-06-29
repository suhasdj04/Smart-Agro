import React, { createContext, useContext, useState, useEffect } from 'react';
import { login as loginApi, logout as logoutApi } from '../api/auth';

const AuthContext = createContext();

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) throw new Error('useAuth must be used within AuthProvider');
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [darkMode, setDarkMode] = useState(() => {
    return localStorage.getItem('smart_agro_dark') === 'true';
  });

  useEffect(() => {
    const savedUser = localStorage.getItem('smart_agro_user');
    const savedToken = localStorage.getItem('smart_agro_token');
    if (savedUser && savedToken) {
      try {
        setUser(JSON.parse(savedUser));
      } catch {
        localStorage.removeItem('smart_agro_user');
        localStorage.removeItem('smart_agro_token');
      }
    }
    setLoading(false);
  }, []);

  const toggleDarkMode = () => {
    setDarkMode((prev) => {
      const next = !prev;
      localStorage.setItem('smart_agro_dark', next.toString());
      return next;
    });
  };

  const login = async (email, password) => {
    const res = await loginApi({ email, password });
    const payload = res.data.data || res.data;
    const { token, user } = payload;
    localStorage.setItem('smart_agro_token', token);
    localStorage.setItem('smart_agro_user', JSON.stringify(user));
    setUser(user);
    return user;
  };

  const logout = async () => {
    try {
      await logoutApi();
    } catch {}
    localStorage.removeItem('smart_agro_token');
    localStorage.removeItem('smart_agro_user');
    setUser(null);
  };

  const updateUser = (updatedUser) => {
    setUser(updatedUser);
    localStorage.setItem('smart_agro_user', JSON.stringify(updatedUser));
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        login,
        logout,
        loading,
        darkMode,
        toggleDarkMode,
        updateUser,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export default AuthContext;
