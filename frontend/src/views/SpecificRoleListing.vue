<template>
  <div class="bg-beige px-10 py-5">
    <div class="flex items-center justify-between">
      <div class="flex items-center flex-nowrap">
        <button @click="goBack">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor"
            class="w-5 h-5">
            <path stroke-linecap="round" stroke-linejoin="round" d="M10.5 19.5L3 12m0 0l7.5-7.5M3 12h18" />
          </svg>
        </button>
        <p class="font-sans pl-4 text-yellow text-2xl">{{ roleName }}</p>
      </div>

      <!-- Edit button -->
      <router-link to="/edit-role-listing"
        class="bg-yellow text-white rounded-full px-4 py-2 flex items-center space-x-2">
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor"
          class="w-4 h-4">
          <path stroke-linecap="round" stroke-linejoin="round"
            d="M16.862 4.487l1.687-1.688a1.875 1.875 0 112.652 2.652L10.582 16.07a4.5 4.5 0 01-1.897 1.13L6 18l.8-2.685a4.5 4.5 0 011.13-1.897l8.932-8.931zm0 0L19.5 7.125M18 14v4.75A2.25 2.25 0 0115.75 21H5.25A2.25 2.25 0 013 18.75V8.25A2.25 2.25 0 015.25 6H10" />
        </svg>
        <span>Edit Role Listing</span>
      </router-link>
    </div>

    <div class="flex items-center flex-nowrap pl-8 text-grey">
      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor"
        class="w-4 h-4">
        <path stroke-linecap="round" stroke-linejoin="round" d="M12 6v6h4.5m4.5 0a9 9 0 11-18 0 9 9 0 0118 0z" />
      </svg>
      <p class="font-sans pl-2 text-grey text-bold">Expires On:</p>
      <p class="font-sans pl-2 text-grey pr-8">{{ expiryDate }}</p>

      <!-- display number of applicants -->
      <!-- <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor"
        class="w-4 h-4 text-green">
        <path stroke-linecap="round" stroke-linejoin="round"
          d="M15.75 6a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0zM4.501 20.118a7.5 7.5 0 0114.998 0A17.933 17.933 0 0112 21.75c-2.676 0-5.216-.584-7.499-1.632z" />
      </svg>
      <p class="font-sans pl-2 text-green">Number Applicants</p> -->

    </div>

    <div class="mt-8 container mx-auto flex items-center justify-between">
      <div>
        <p class="text-bold">Reporting Manager</p>
        <p>{{ managerName }}</p>
      </div>
      <div>
        <p class="text-bold">Hiring Department</p>
        <p>{{ department }}</p>
      </div>
      <div>
        <p class="text-bold">Country</p>
        <p>{{ country }}</p>
      </div>
    </div>

    <div class="mt-16 p-10">
      <div class="grid grid-cols-2">
        <div>
          <p class=" text-bold">Description</p>
          <p class="pr-8">{{ description }}</p>
        </div>
        <div>
          <p class="text-bold">Required Skills</p>
          <ul class="list-disc pl-4">
            <li v-for="skill in skills" :key="skill">{{ skill }}</li>
          </ul>
        </div>
      </div>
    </div>

  </div>
</template>

<script>
import axios from "axios";

const rolelistingID = 1

export default {
  name: 'SpecificRoleListing',
  components: {},
  props: {
  },
  data() {
    return {
      roleName: "",
      expiryDate: "",
      managerId: null,
      managerName: "",
      department: "",
      country: "",
      skills: [],
      description: "",
    };
  },
  methods: {
    getRoleListingInfo() {
      axios
        .get(`http://127.0.0.1:5000/rolelisting/${rolelistingID}`)
        .then((response) => {
          // console.log(response.data.data[rolelistingID])
          this.roleName = response.data.data[rolelistingID]["role_name"]
          this.expiryDate = response.data.data[rolelistingID]["application_deadline"]
          this.managerId = response.data.data[rolelistingID]["manager_ID"]
          this.department = response.data.data[rolelistingID]["dept"]
          this.country = response.data.data[rolelistingID]["country"]

          // set managerName variable after obtaining managerId
          this.getStaffName();

          // set skills variable after obtaining roleName
          this.getRoleSkills();

          // set description variable after obtaining roleName
          this.getRoleDescription();
        })
        .catch((error) => {
          console.log(error.message);
        });
    },
    getStaffName() {
      axios
        .get(`http://127.0.0.1:5000/staff/${this.managerId}`)
        .then((response) => {
          const managerData = response.data.data[this.managerId];
          if (managerData) {
            this.managerName = managerData["staff_FName"] + " " + managerData["staff_LName"];
          }
        })
        .catch((error) => {
          console.log(error.message);
        });
    },
    getRoleSkills() {

      axios
        .get(`http://127.0.0.1:5000/get_role_skill/${this.roleName}`)
        .then((response) => {
          const roleSkillsData = response.data.data;
          // console.log(roleSkillsData)
          if (roleSkillsData) {
            this.skills = roleSkillsData;
          }
        })
        .catch((error) => {
          console.log(error.message);
        });
    },
    getRoleDescription() {

      axios
        .get(`http://127.0.0.1:5000/get_all_role`)
        .then((response) => {
          const roleDescriptionsData = response.data.data
          for (const role of roleDescriptionsData) {
            for (let rName in role) {
              if (rName == this.roleName) {
                this.description = role[this.roleName]
              }
            }
          }
          // const roleDescription = response.data.data[$roleName];
          // console.log(roleDescription)
          // if (roleDescription) {
          //   this.description = roleDescription;
          // }
        })
        .catch((error) => {
          console.log(error.message);
        });
    }
  },
  created() {
    this.getRoleListingInfo();
  }
}
</script>

<style></style>