<template>
  <div class="min-h-screen bg-beige">
    <Logout class="px-10 mb-3"/>
    <router-view class="px-10"></router-view>
  </div>
</template>

<script setup>
import Logout from '@/components/Logout.vue'
</script>