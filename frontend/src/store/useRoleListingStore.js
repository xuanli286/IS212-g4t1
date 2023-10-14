// roleListingStore.js
import { defineStore } from "pinia";

// Define the role listing store
export const useRoleListingStore = defineStore({
  id: "roleListing",
  state: () => ({
    roleListingId: null, // Initialize role listing ID as null
  }),
  actions: {
    setRoleListingId(roleListingId) {
      this.roleListingId = roleListingId;
    },
    clearRoleListingId() {
      this.roleListingId = null;
    },
  },
});
