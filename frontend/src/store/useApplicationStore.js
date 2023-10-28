// roleListingStore.js
import { defineStore } from "pinia";

// Define the role listing store
export const useApplicationStore = defineStore({
  id: "staffId",
  state: () => ({
    staffId: null, // Initialize staff ID as null
  }),
  actions: {
    setStaffId(staffId) {
      this.staffId = staffId;
    },
    clearStaffId() {
      this.staffId = null;
    },
  },
});
