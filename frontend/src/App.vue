<template>
  <div class="min-h-screen bg-beige">
    <Logout v-if="user" class="px-10 mb-3" />
    <router-view class="px-10"></router-view>
  </div>
</template>

<script setup>
import { useUserStore } from '@/store/useUserStore.js';
import { storeToRefs } from 'pinia';

const userStore = useUserStore();
const {
  user,
} = storeToRefs(userStore);
</script>