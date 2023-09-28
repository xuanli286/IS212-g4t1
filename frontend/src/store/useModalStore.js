import { ref } from 'vue';
import { defineStore } from 'pinia';

export const useModalStore = defineStore('Modal', () => {
  const isOpen = ref(false);
  const isSuccess = ref(false);

  return {
    isOpen,
    isSuccess,
  }
})
