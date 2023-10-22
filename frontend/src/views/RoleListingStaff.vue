<script>
import axios from "axios";
import { useRoleListingStore } from '@/store/useRoleListingStore';
import { useConstantStore } from '@/store/useConstantStore';
import { useUserStore } from '@/store/useUserStore';
import router from "@/router";
import { isSubset } from "@/utils/isSubset";

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
  methods: {
    async fetchData() {
      const constStore = useConstantStore();
      const { backend_url, countries, hiringDepartment } = constStore;
      const userStore = useUserStore();
      const { user } = userStore;

      const openResponse =
        await axios.get(`${backend_url}/openrolelisting`)
          .catch(() => {
            return { data: { data: {} } }
          });
      const staffResponse = await axios.get(`${backend_url}/staff`);

      const skillResponse = await axios.get(`${backend_url}/get_staff_skill/${user.staff_ID}`)
      this.userSkills = skillResponse.data.data

      this.roleListings = this.processListings(openResponse.data.data.rolelisting);
      for (let key of Object.keys(this.roleListings)) {
        this.applications[key] =
          await axios.get(`${backend_url}/applications/${key}`)
            .then((response) => {
              return response.data.data.length
            })
            .catch(() => {
              return 0
            })
      }
      this.staffNames = this.processStaff(staffResponse.data.data.staff);

      this.countries = countries

      this.hiringDepartments = hiringDepartment



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
    updateRoleListingId(id) {
      useRoleListingStore().setRoleListingId(id);
      router.push('/viewspecificrolelisting/' + id);
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
    async updateFilter(){
      var filteredListings = {}
      const backend_url = useConstantStore().backend_url;
      var listings =
        await axios.get(`${backend_url}/openrolelisting`)
        .then((response) => {
          return response.data.data.rolelisting
        })
        .catch(() => {
          return []
        });
      
      for(let listing of listings){
        let listingId = Object.keys(listing)[0]
        var listingSkills = 
          await axios.get(`${backend_url}/get_role_skill/${listing[listingId].role_name}`)
          .then((response) => {
            return response.data.data
          })
          .catch(() => {
            return []
          });

        if(isSubset(this.selectedSkills, listingSkills) && (this.selectedCountry == listing[listingId].country || this.selectedCountry == "all") && (this.selectedDept == listing[listingId].dept || this.selectedDept == "all")){
          filteredListings[listingId] = listing[listingId]
        }
      }
      this.roleListings = filteredListings
    },
    clearFilter(){
      this.selectedCountry = "all"
      this.selectedDept = "all"
      this.selectedSkills = []
      this.fetchData()
    }
  },
  created() {
    this.fetchData();
  },

};
</script>


<template>
  <div class="bg-beige px-10 py-5">
    <div>
      <h1 class="text-xl font-serif text-center py-20" id="title">Find Your Next Role With Us</h1>
    </div>

    <!-- card starts here -->
    <div class="flex flex-row">
      <div class="p-10 me-5 bg-white rounded-xl w-1/3">
        <div class="font-serif text-green text-xl">Filter</div>
        <select class="mt-7 p-2 rounded-md w-full outline outline-1" @change="updateFilter()" v-model="selectedCountry" id="country">
            <option selected disabled value="all"> Country </option>
            <option v-for="country of countries" :value=country> {{ country }}</option>
        </select>
        <select class="mt-7 p-2 rounded-md w-full outline outline-1" @change="updateFilter()" v-model="selectedDept" id="department">
            <option selected disabled value="all"> Hiring Department </option>
            <option v-for="dept of hiringDepartments" :value="dept"> {{ dept }}</option>
        </select>

        <div class="my-10 flex flex-col">
          <span>REQUIRED SKILLS</span> 
          <div><input type="checkbox" v-model="selectAllSkills"> Select All</div>
          <div v-for="skill of userSkills">
            <input @change="updateFilter()" type="checkbox" class="skill" :value=skill v-model="selectedSkills"> {{ skill }} 
          </div>
        </div>

        <button type="button" @click="clearFilter()" class="w-full outline outline-yellow-1 py-2 px-5 rounded-lg text-sm text-yellow font-serif btn hover:bg-yellow hover:text-white focus:ring-4 focus:ring-yellow-300">
          Clear All Filters
        </button>
      </div>

      <!-- card ends here -->
      <div class="w-full">
        <ul class="rolelisting-container">
          <li v-if="Object.keys(roleListings).length == 0" class="py-5 text-center">
            <div class="grow"></div>
            <div class="font-bold">No matching roles available!</div>
            <div class="grow"></div>
          </li>
          <li v-else v-for="(listing, id) in roleListings" :key="id"
            class="rolelisting-panel flex border-t py-5 hover:bg-grey-50">
            <router-link :to="'/viewspecificrolelisting/' + id" @click=updateRoleListingId(id) :id="'rolelisting-' + id">
              <div class="flex-none h-100">
                <div class="role-title text-yellow text-xl"> {{ listing.role_name }} </div>
                <div class="role-manager text-base"> Reporting Manager: {{ getManagerName(listing.manager_ID) }} </div>
                <div class="flex flex-row text-xs">
                  <div class="role-deadline text-grey"> Apply by {{ formatDate(listing.application_deadline) }}</div>
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
                <div class="role-department flex bg-yellow mx-2 h-1 w-1 rounded-full"> </div>
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