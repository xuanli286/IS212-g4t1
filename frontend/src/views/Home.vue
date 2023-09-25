<template>
  <div>
    <h1>Home</h1>
    <div v-if="user">
      <h2>User Data:</h2>
      <p>Access ID: {{ user.access_ID }}</p>
      <p>First Name: {{ user.staff_FName }}</p>
      <p>Last Name: {{ user.staff_LName }}</p>
    </div>
    <div v-else>
      <p>No user data available.</p>
    </div>
  </div>
</template>

<script>
import { useUserStore } from '@/store/userStore.js';


export default {
  name: 'Home',
  components: {},
  props: {
  },
  data() {
    return {
    };
  },
  methods: {
  },
  computed: {
    user() {
      const userStore = useUserStore();
      return userStore.user;
    },
  },
  created() {
  },
}
</script>

<style></style>