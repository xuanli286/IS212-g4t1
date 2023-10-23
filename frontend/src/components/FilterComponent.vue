<template>
    <div class="p-10 me-5 bg-white rounded-xl w-1/3">
      <div class="font-serif text-green text-xl">Filter</div>
      <select class="mt-7 p-2 rounded-md w-full outline outline-1" @change="updateFilter()" v-model="selectedCountry" id="country">
        <option selected disabled value="all">Country</option>
        <option v-for="country in countries" :value="country">{{ country }}</option>
      </select>
      <select class="mt-7 p-2 rounded-md w-full outline outline-1" @change="updateFilter()" v-model="selectedDept" id="department">
        <option selected disabled value="all">Hiring Department</option>
        <option v-for="dept in hiringDepartments" :value="dept">{{ dept }}</option>
      </select>

      <div class="my-10 flex flex-col">
        <span>REQUIRED SKILLS</span> 
        <div>
          <input type="checkbox" v-model="selectAllSkills"> Select All
        </div>
        <div v-for="skill in userSkills" :key="skill">
          <input @change="updateFilter()" type="checkbox" class="skill" :value="skill" v-model="selectedSkills"> {{ skill }} 
        </div>
      </div>

      <button type="button" @click="clearFilter()" class="w-full outline outline-yellow-1 py-2 px-5 rounded-lg text-sm text-yellow font-serif btn hover:bg-yellow hover:text-white focus:ring-4 focus:ring-yellow-300">
        Clear All Filters
      </button>
    </div>
</template>

<script>

export default {
  data() {
    return {
      selectedCountry: "all",
      selectedDept: "all",
      selectAllSkills: false,
      selectedSkills: [],
    };
  },
  props: {
    countries: Array, 
    hiringDepartments: Array, 
    userSkills: Array, 
  },
  methods: {
    async updateFilter(){
      this.$emit('filter-updated', {
        selectedCountry: this.selectedCountry,
        selectedDept: this.selectedDept,
        selectedSkills: this.selectedSkills,
      });
    },
    clearFilter(){
      this.selectedCountry = "all"
      this.selectedDept = "all"
      this.selectedSkills = []
      this.$emit('filter-cleared');
    }
  },
};
</script>