<template>
  <div>
    <div v-if="user">
      <RoleListingManagement v-if="user.access_ID > 0"/>
    </div>
    <div v-else>
      <p>No user data available.</p>
    </div>
  </div>
</template>

<script>
import { useUserStore } from '@/store/useUserStore.js';
import RoleListingManagement from "../views/RoleListingManagement.vue";

export default {
  name: 'Home',
  components: {
    RoleListingManagement,
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