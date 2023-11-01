<template>
    <div class="p-10 me-5 bg-white rounded-xl w-1/3 border-4 border-yellow">
      <div class="font-serif text-green text-xl">Filter</div>

      <select v-if="inCandidates" class="mt-7 p-2 rounded-md w-full outline outline-1" @change="updateFilter()" v-model="selectedRoleListing" id="rolelisting">
        <option selected disabled value="">Listed Role</option>
        <option v-for="(rolelisting, index) in roleListings" :key="index" :value="rolelisting">{{ rolelisting }}</option>
      </select>

      <select class="mt-7 p-2 rounded-md w-full outline outline-1" @change="updateFilter()" v-model="selectedCountry" id="country">
        <option selected disabled value="all">Country</option>
        <option v-for="(country, index) in countries" :key="index" :value="country">{{ country }}</option>
      </select>

      <select class="mt-7 p-2 rounded-md w-full outline outline-1" @change="updateFilter()" v-model="selectedDept" id="department">
        <option selected disabled value="all">Hiring Department</option>
        <option v-for="(dept, index) in hiringDepartments" :key="index" :value="dept">{{ dept }}</option>
      </select>

      <div v-if="inManagement" class="my-10 flex flex-col">
        <span>STATUS</span> 
        <div v-for="status in statuses" :key="status">
          <input @change="updateFilter()" type="checkbox" class="status" :value="status" v-model="selectedStatus" :id="`${status}`"> {{ status }} 
        </div>
      </div>

      <div class="my-10 flex flex-col">
        <span>REQUIRED SKILLS</span> 
        <div class="h-72 overflow-y-auto">
          <div>
            <input type="checkbox" v-model="selectAllSkills"> Select All
          </div>
          <div v-if="inCandidates" v-for="roleSkill in roleSkils" :key="roleSkill">
            <input @change="updateFilter()" type="checkbox" class="skill" :value="roleSkill" v-model="selectedSkills" :id="`${roleSkill}`"> {{ roleSkill }} 
          </div>
          <div v-else v-for="skill in userSkills" :key="skill">
            <input @change="updateFilter()" type="checkbox" class="skill" :value="skill" v-model="selectedSkills" :id="`${skill}`"> {{ skill }} 
          </div>
        </div>
        
      </div>

      <button type="button" @click="clearFilter()" class="w-full outline outline-yellow-1 py-2 px-5 rounded-lg text-sm text-yellow font-serif btn hover:bg-yellow hover:text-white focus:ring-4 focus:ring-yellow-300" id="clearFilterButton">
        Clear All Filters
      </button>
    </div>
</template>

<script>
import { useConstantStore } from "@/store/useConstantStore";
import { useUserStore } from "@/store/useUserStore";
import axios from "axios";

export default {
  data() {
    return {
      selectedCountry: "all",
      selectedDept: "all",
      selectedRoleListing: "",
      selectAllSkills: true,
      selectedSkills: [],
      selectedStatus: [],
      statuses: ["Open","Closed"],
      roleSkils: [],
    };
  },
  setup() {
    const user = useUserStore().user;

    const backend_url = useConstantStore().backend_url;

    return {user, backend_url}
  },
  props: {
    countries: Array, 
    hiringDepartments: Array, 
    userSkills: Array,
    roleListings: Array, 
    inManagement: Boolean,
    inCandidates: Boolean
  },
  created() {
    if (this.inCandidates) {
      this.getSkills();
    }
  },
  methods: {
    async updateFilter(){

      console.log(this.roleSkils.length);
      this.$emit('filter-updated', {
        selectedCountry: this.selectedCountry,
        selectedDept: this.selectedDept,
        selectedStatus: this.selectedStatus,
        selectedSkills: this.selectedSkills,
        selectedRoleListing: this.selectedRoleListing,
        
      });
    },
    clearFilter(){
      this.selectedCountry = "all"
      this.selectedDept = "all"
      this.selectedStatus= []
      this.selectedSkills = []
      this.selectedRoleListing = ""
      this.roleSkils = []
      this.selectAllSkills = true
      this.$emit('filter-cleared');
    },
    getSkills() {
      axios.get(`${this.backend_url}/get_role_skill/${this.selectedRoleListing}`)
           .then(response => {
            this.roleSkils = response.data.data;
           })
           .catch (error => {
            console.error(error)
           })
    }
  },
  watch: {
    selectedRoleListing : "getSkills",
    selectedSkills: function(newSkills) {
      if (newSkills.length > 0) {
        this.selectAllSkills = false; 
      }
    },
  }
};
</script>