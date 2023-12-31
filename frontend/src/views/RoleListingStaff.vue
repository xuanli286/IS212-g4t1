<script>
import axios from "axios";
import { useRoleListingStore } from "@/store/useRoleListingStore";
import { useConstantStore } from "@/store/useConstantStore";
import { useUserStore } from "@/store/useUserStore";
import router from "@/router";
import { isSubset } from "@/utils/isSubset";
import FilterComponent from "@/components/FilterComponent.vue";
import SearchComponent from "@/components/SearchComponent.vue";

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
      searchQuery: "",
    };
  },
  components: {
    FilterComponent,
    SearchComponent,
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
      if(openResponse.data.data.rolelisting != null){      
        this.roleListings = this.processListings(openResponse.data.data.rolelisting)
      }

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
    async searchRoles(searchQuery) {
      // need to update this so that it will axios call
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
          listing[listingId].role_name
            .toLowerCase()
            .includes(searchQuery.toLowerCase()) ||
          listing[listingId].dept.toLowerCase() === searchQuery.toLowerCase() ||
          listing[listingId].country.toLowerCase() ===
            searchQuery.toLowerCase() ||
          listingSkills.some(
            (skill) => skill.toLowerCase() === searchQuery.toLowerCase()
          )
        ) {
          filteredListings[listingId] = listing[listingId];
          // console.log(filteredListings, "filtered")
        }
      }
      this.roleListings = filteredListings;
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

    <search-component
      @search-updated="searchRoles($event)"
      :search="searchQuery"
    >
    </search-component>

    <div class="flex flex-row">
      <filter-component
        :countries="countries"
        :hiringDepartments="hiringDepartments"
        :userSkills="userSkills"
        :inManagement="false"
        @filter-updated="updateFilter"
        @filter-cleared="clearFilter"
      ></filter-component>

      <div class="w-full">
        <ul class="rolelisting-container">
          <li
            v-if="Object.keys(roleListings).length == 0"
            class="py-5 text-center message"
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
              <div class="flex-none h-100" @click="updateRoleListingId(id)">
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
                <div class="font-bold role-department">{{ listing.dept }}</div>
                <div class="flex bg-yellow mx-2 h-1 w-1 rounded-full"></div>
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
