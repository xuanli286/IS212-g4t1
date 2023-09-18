import { ref } from 'vue';
import { defineStore } from 'pinia';

export const useEditRoleListingStore = defineStore('editRoleListing', () => {
  const isOpen = ref(false);
  const isSuccess = ref(false);

  return {
    isOpen,
    isSuccess,
  }
})
