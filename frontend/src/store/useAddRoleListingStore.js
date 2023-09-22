import { ref } from 'vue';
import { defineStore } from 'pinia';

export const useAddRoleListingStore = defineStore('addRoleListing', () => {
  const isOpen = ref(false);
  const isSuccess = ref(false);

  return {
    isOpen,
    isSuccess,
  }
})
