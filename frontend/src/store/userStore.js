// userStore.js
import { defineStore } from 'pinia';

// Define the user store
export const useUserStore = defineStore({
  id: 'user',
  state: () => ({
    user: null, // Initialize user data as null
  }),
  actions: {
    setUser(userData) {
      this.user = userData;
    },
    clearUser() {
      this.user = null;
    },
  },
});