import { defineStore } from 'pinia';
import { login as loginApi, register as registerApi } from '../api/auth';

export const useUserStore = defineStore('user', {
  state: () => ({
    user: JSON.parse(localStorage.getItem('user')) || null,
    token: localStorage.getItem('token') || null,
  }),
  getters: {
    isLoggedIn: (state) => !!state.token,
    isTeacher: (state) => state.user?.role === 'teacher',
    isStudent: (state) => state.user?.role === 'student',
  },
  actions: {
    async login(credentials) {
      try {
        const response = await loginApi(credentials);
        this.token = response.access_token;
        localStorage.setItem('token', this.token);
        
        // In a real app, you'd fetch user profile here. 
        // For now, let's decode the token or just set a dummy user.
        // We'll assume the API returns user info in the token or we need a separate call.
        // For simplicity, let's just set a dummy user based on the username for now.
        const user = {
          username: credentials.username,
          role: credentials.username === 'admin' ? 'teacher' : 'student'
        };
        this.user = user;
        localStorage.setItem('user', JSON.stringify(user));
        return user;
      } catch (error) {
        throw error;
      }
    },
    async register(userData) {
      try {
        await registerApi(userData);
      } catch (error) {
        throw error;
      }
    },
    logout() {
      this.user = null;
      this.token = null;
      localStorage.removeItem('token');
      localStorage.removeItem('user');
    }
  }
});
