<template>
  <div>
    <div v-if="user">
      <RoleListingStaff />
    </div>
    <div v-else>
      <p>No user data available.</p>
    </div>
  </div>
</template>

<script>
import { useUserStore } from '@/store/useUserStore.js';
import RoleListingStaff from "../views/RoleListingStaff.vue";

export default {
  name: 'Home',
  components: {
    RoleListingStaff,
  },
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