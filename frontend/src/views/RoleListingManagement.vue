<script>
import axios from "axios";
import { useRoleListingStore } from '@/store/useRoleListingStore';
import { useConstantStore } from '@/store/useConstantStore';
import router from "@/router";

export default {
  data() {
    return {
      roleListings: {},
      staffNames: {},
      applications: {}
    };
  },
  methods: {
    async fetchData() {
      const constStore = useConstantStore();
      const { backend_url } = constStore;

      const openResponse =
        await axios.get(`${backend_url}/openrolelisting`)
          .catch(() => {
            return { data: { data: {} } }
          });
      const closeResponse =
        await axios.get(`${backend_url}/closerolelisting`)
          .catch(() => {
            return { data: { data: {} } }
          });
      const staffResponse = await axios.get(`${backend_url}/staff`);

      this.roleListings = this.processListings(openResponse.data.data.rolelisting.concat(closeResponse.data.data.rolelisting));
      for (let key of Object.keys(this.roleListings)) {
        this.applications[key] =
          await axios.get(`${backend_url}/applications/${key}`)
            .then((response) => {
              return response.data.data.length
            })
            .catch((error) => {
              return 0
            })
      }
      this.staffNames = this.processStaff(staffResponse.data.data.staff);

    },
    checkOpen(listing) {
      const today = new Date();
      const deadline = new Date(listing.application_deadline);
      return deadline > today;
    },
    formatDate(dateString) {
      const date = new Date(dateString);
      const day = date.getDate();
      const month = date.toLocaleString('default', { month: 'long' });
      const year = date.getFullYear();
      return `${day} ${month} ${year}`;
    },
    getManagerName(id) {
      try {
        const FName = this.staffNames[id].split(" ")[0];
        const LName = this.staffNames[id].split(" ")[1][0];
        return `${FName} ${LName}.`;
      } catch (error) {
        return "";
      }
    },
    processListings(listings) {
      const processedListings = {};
      for (const listing of listings) {
        for (const key in listing) {
          processedListings[key] = listing[key];
        }
      }
      return processedListings;
    },
    processStaff(staffData) {
      const processedStaff = {};
      for (const staff of staffData) {
        for (const key in staff) {
          if (staff[key]) {
            processedStaff[key] = staff[key]['staff_FName'] + " " + staff[key]['staff_LName'];
          }
        }
      }
      return processedStaff;
    },
    viewListing(id) {
      useRoleListingStore().setRoleListingId(id);
      router.push('/specificrolelisting/' + id);
    },
    viewApplicants(id) {
      useRoleListingStore().setRoleListingId(id);
      router.push('/applicants/' + id);
    },
  },
  created() {
    this.fetchData();
  },

};
</script>

<template>
  <div class="bg-beige px-10 py-5">
    <div class="flex flex-row mx-64">
      <div class="flex flex-row grow py-20 text-xl font-serif text-center " id="roleListings">
        <div class="grow"></div>
        <h1 class="translate-x-[85px]">Manage Role Listing</h1>
        <div class="grow"></div>
      </div>
      <div class="flex items-center">
        <router-link id="addRoleListingButton" to="/addrolelisting"
          class="flex flex-row bg-yellow py-2 px-5 rounded-full text-white text-sm">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor"
            class="w-6 h-6 me-2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v6m3-3H9m12 0a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <div class="my-auto">Add Role Listing</div>
        </router-link>
      </div>
    </div>
    <ul class="mx-64 min-w-fit rolelisting-container">
      <li v-if="Object.keys(roleListings).length == 0" class="py-5 text-center">
        <div class="grow"></div>
        <div class="font-bold">No listings available!</div>
        <div class="grow"></div>
      </li>
      <li v-else v-for="(listing, id) in roleListings" :key="id"
        class="rolelisting-panel flex border-t py-5 hover:bg-grey-50 cursor-pointer" @click="viewListing(id)">
        <div class="flex-none h-100">
          <div class="role-title text-yellow text-xl"> {{ listing.role_name }} </div>
          <div class="role-manager text-base"> Reporting Manager: {{ getManagerName(listing.manager_ID) }} </div>
          <div class="flex flex-row text-xs">
            <div class="role-deadline text-grey"> Apply by {{ formatDate(listing.application_deadline) }}</div>
            <div class="flex items-center mx-2">
              <span class="bg-black h-1 w-1 rounded-full"></span>
            </div>
            <div id="numberApplicants" class="role-applicants font-bold text-green hover:underline cursor-pointer"
              @click.stop="viewApplicants(id)">
              {{ applications[id] }}
              <span v-if="applications[id] == 1"> applicant </span>
              <span v-else> applicants </span>
            </div>
          </div>
        </div>
        <div class="grow"></div>
        <div>
          <div class="flex flex-row">
            <div class="grow"></div>
            <div :class="{ 'bg-green': checkOpen(listing), 'bg-red': !checkOpen(listing) }"
              class="role-status me-5 text-xs px-4 py-1 rounded-full text-white">
              <span v-if="checkOpen(listing)">Open</span>
              <span v-else>Closed</span>
            </div>
          </div>
          <div class="flex flex-row items-center text-yellow pt-3">
            <div class="font-bold">{{ listing.dept }}</div>
            <div class="role-department flex bg-yellow mx-2 h-1 w-1 rounded-full"> </div>
            <div class="role-country">{{ listing.country }}</div>
          </div>
        </div>
      </li>
    </ul>
  </div>
</template>

<style></style>