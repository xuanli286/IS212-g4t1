<script>
import axios from "axios";
import { useRoleListingStore } from "@/store/useRoleListingStore";
import { useConstantStore } from "@/store/useConstantStore";
import { useUserStore } from "@/store/useUserStore";
import router from "@/router";
import { isSubset } from "@/utils/isSubset";
import FilterComponent from "@/components/FilterComponent.vue";

export default {
  data() {
    return {
      roleListings: {},
      staffNames: {},
      applications: {},
      countries: [],
      hiringDepartments: [],
      selectedCountry: "all",
      selectedDept: "all",
      selectedSkills: [],
      staffId: {},
    };
  },
  components: {
    FilterComponent,
  },
  methods: {
    async fetchData() {
      const constStore = useConstantStore();
      const { backend_url, countries, hiringDepartment } = constStore;
      const userStore = useUserStore();
      const { user } = userStore;

      const openResponse = await axios
        .get(`${backend_url}/openrolelisting`)
        .catch(() => {
          return { data: { data: {} } };
        });
      const staffResponse = await axios.get(`${backend_url}/staff`);

      const skillResponse = await axios.get(
        `${backend_url}/get_staff_skill/${user.staff_ID}`
      );
      this.userSkills = skillResponse.data.data;

      this.roleListings = this.processListings(
        openResponse.data.data.rolelisting
      );
      for (let key of Object.keys(this.roleListings)) {
        this.applications[key] = await axios
          .get(`${backend_url}/applications/${key}`)
          .then((response) => {
            return response.data.data.length;
          })
          .catch(() => {
            return 0;
          });
      }
      this.staffNames = this.processStaff(staffResponse.data.data.staff);

      this.countries = countries;

      this.hiringDepartments = hiringDepartment;
    },
    checkOpen(listing) {
      const today = new Date();
      const deadline = new Date(listing.application_deadline);
      return deadline > today;
    },
    formatDate(dateString) {
      const date = new Date(dateString);
      const day = date.getDate();
      const month = date.toLocaleString("default", { month: "long" });
      const year = date.getFullYear();
      return `${day} ${month} ${year}`;
    },
    updateRoleListingId(id) {
      useRoleListingStore().setRoleListingId(id);
      router.push("/viewspecificrolelisting/" + id);
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
            processedStaff[key] =
              staff[key]["staff_FName"] + " " + staff[key]["staff_LName"];
          }
        }
      }
      return processedStaff;
    },
    async updateFilter(data) {
      this.selectedCountry = data.selectedCountry;
      this.selectedDept = data.selectedDept;
      this.selectedSkills = data.selectedSkills;

      var filteredListings = {};
      const backend_url = useConstantStore().backend_url;
      var listings = await axios
        .get(`${backend_url}/openrolelisting`)
        .then((response) => {
          return response.data.data.rolelisting;
        })
        .catch(() => {
          return [];
        });

      for (let listing of listings) {
        let listingId = Object.keys(listing)[0];
        var listingSkills = await axios
          .get(`${backend_url}/get_role_skill/${listing[listingId].role_name}`)
          .then((response) => {
            return response.data.data;
          })
          .catch(() => {
            return [];
          });

        if (
          isSubset(this.selectedSkills, listingSkills) &&
          (this.selectedCountry == listing[listingId].country ||
            this.selectedCountry == "all") &&
          (this.selectedDept == listing[listingId].dept ||
            this.selectedDept == "all")
        ) {
          filteredListings[listingId] = listing[listingId];
        }
      }
      this.roleListings = filteredListings;
    },
    clearFilter() {
      this.selectedCountry = "all";
      this.selectedDept = "all";
      this.selectedSkills = [];
      this.fetchData();
    },
  },
  created() {
    this.fetchData();
  },
};
</script>


<template>
  <div class="bg-beige px-10">
    <div>
      <h1 class="text-xl font-serif text-center py-10" id="title">
        Find Your Next Role With Us
      </h1>
    </div>

    <!-- search bar -->
    <div>
      <form class="flex items-center pb-10">
        <label for="simple-search" class="sr-only">Search</label>
        <div class="relative w-full">
          <div
            class="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none"
          >
            <svg
              class="w-4 h-4 text-gray-500 dark:text-gray-400"
              aria-hidden="true"
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 18 20"
            >
              <path
                stroke="currentColor"
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M3 5v10M3 5a2 2 0 1 0 0-4 2 2 0 0 0 0 4Zm0 10a2 2 0 1 0 0 4 2 2 0 0 0 0-4Zm12 0a2 2 0 1 0 0 4 2 2 0 0 0 0-4Zm0 0V6a3 3 0 0 0-3-3H9m1.5-2-2 2 2 2"
              />
            </svg>
          </div>
          <input
            type="text"
            id="simple-search"
            class="bg-gray-50 border border-yellow text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full pl-10 p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 text-black dark:focus:ring-blue-500 dark:focus:border-blue-500"
            placeholder="Search Roles"
            required
          />
        </div>
        <button
          type="submit"
          class="p-2.5 ml-2 text-sm font-medium text-blue bg-yellow rounded-lg border border-blue-700 hover:bg-yellow focus:ring-4 focus:outline-none focus:ring-yellow-300 dark:bg-yellow-600 dark:hover:bg-yellow-700 dark:focus:ring-yellow-800"
        >
          <svg
            class="w-4 h-4"
            aria-hidden="true"
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 20 20"
          >
            <path
              stroke="currentColor"
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="m19 19-4-4m0-7A7 7 0 1 1 1 8a7 7 0 0 1 14 0Z"
            />
          </svg>
          <span class="sr-only">Search</span>
        </button>
      </form>
    </div>

    <div class="flex flex-row">
      <filter-component
        :countries="countries"
        :hiringDepartments="hiringDepartments"
        :userSkills="userSkills"
        @filter-updated="updateFilter"
        @filter-cleared="clearFilter"
      ></filter-component>

      <div class="w-full">
        <ul class="rolelisting-container">
          <li
            v-if="Object.keys(roleListings).length == 0"
            class="py-5 text-center"
          >
            <div class="grow"></div>
            <div class="font-bold">No matching roles available!</div>
            <div class="grow"></div>
          </li>
          <li
            v-else
            v-for="(listing, id) in roleListings"
            :key="id"
            class="rolelisting-panel flex border-t py-5 hover:bg-grey-50"
          >
            <router-link
              :to="'/viewspecificrolelisting/' + id"
              @click="updateRoleListingId(id)"
              :id="'rolelisting-' + id"
            >
              <div class="flex-none h-100">
                <div class="role-title text-yellow text-xl">
                  {{ listing.role_name }}
                </div>
                <div class="role-manager text-base">
                  Reporting Manager: {{ getManagerName(listing.manager_ID) }}
                </div>
                <div class="flex flex-row text-xs">
                  <div class="role-deadline text-grey">
                    Apply by {{ formatDate(listing.application_deadline) }}
                  </div>
                  <div class="flex items-center mx-2">
                    <span class="bg-black h-1 w-1 rounded-full"></span>
                  </div>
                  <div class="role-applicants font-bold text-green">
                    {{ applications[id] }}
                    <span v-if="applications[id] == 1"> applicant </span>
                    <span v-else> applicants </span>
                  </div>
                </div>
              </div>
            </router-link>
            <div class="grow"></div>
            <div>
              <div class="flex flex-row">
                <div class="grow"></div>
              </div>
              <div class="flex flex-row items-center text-yellow pt-3">
                <div class="font-bold">{{ listing.dept }}</div>
                <div
                  class="role-department flex bg-yellow mx-2 h-1 w-1 rounded-full"
                ></div>
                <div class="role-country">{{ listing.country }}</div>
              </div>
            </div>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<style></style>