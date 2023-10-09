<template>
  <div class="bg-beige px-10 py-5">
    <div class="flex items-center justify-between">
      <div class="flex items-center flex-nowrap">
        <button @click="goBack">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            stroke-width="1.5"
            stroke="currentColor"
            class="w-5 h-5"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              d="M10.5 19.5L3 12m0 0l7.5-7.5M3 12h18"
            />
          </svg>
        </button>
        <p class="font-sans pl-4 text-yellow text-2xl">{{ roleName }}</p>
      </div>

      <!-- Edit button -->
      <router-link
        to="/edit-role-listing"
        class="bg-yellow text-white rounded-full px-4 py-2 flex items-center space-x-2"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
          stroke-width="1.5"
          stroke="currentColor"
          class="w-4 h-4"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            d="M16.862 4.487l1.687-1.688a1.875 1.875 0 112.652 2.652L10.582 16.07a4.5 4.5 0 01-1.897 1.13L6 18l.8-2.685a4.5 4.5 0 011.13-1.897l8.932-8.931zm0 0L19.5 7.125M18 14v4.75A2.25 2.25 0 0115.75 21H5.25A2.25 2.25 0 013 18.75V8.25A2.25 2.25 0 015.25 6H10"
          />
        </svg>
        <span>Edit Role Listing</span>
      </router-link>

      <!-- Modal toggle -->
      <button
        class="bg-yellow text-white rounded-full px-4 py-2 flex items-center space-x-2"
        type="button"
        @click="openApply"
      >
        Apply for Role
      </button>
      <!-- Main modal -->
      <div
        id="authentication-modal"
        aria-hidden="true"
        class="hidden overflow-x-hidden overflow-y-auto fixed h-modal md:h-full top-4 left-0 right-0 md:inset-0 z-50 items-center"
      >
        <div class="relative w-full max-w-xxl pt-12 h-full md:h-auto">
          <!-- Modal content -->
          <div class="bg-white rounded-lg shadow relative">
            <div class="flex justify-end p-2">
              <button
                type="button"
                class="text-gray-400 bg-transparent hover:bg-gray-200 hover:text-gray-900 rounded-lg text-sm p-1.5 ml-auto inline-flex items-center dark:hover:bg-gray-800 dark:hover:text-white"
                @click="closeApply"
              >
                <svg
                  class="w-5 h-5"
                  fill="currentColor"
                  viewBox="0 0 20 20"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <path
                    fill-rule="evenodd"
                    d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
                    clip-rule="evenodd"
                  ></path>
                </svg>
              </button>
            </div>
            <form
              class="space-y-6 px-6 lg:px-8 pb-4 sm:pb-6 xl:pb-8"
              action="#"
            >
              <h3 class="text-xl font-medium text-gray-900 dark:text-white">
                Sign in to our platform
              </h3>
              <div>
                <label
                  for="email"
                  class="text-sm font-medium text-gray-900 block mb-2 dark:text-gray-300"
                  >Your email</label
                >
                <input
                  type="email"
                  name="email"
                  id="email"
                  class="bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-600 dark:border-gray-500 dark:placeholder-gray-400 dark:text-white"
                  placeholder="name@company.com"
                  required=""
                />
              </div>
              <div>
                <label
                  for="password"
                  class="text-sm font-medium text-gray-900 block mb-2 dark:text-gray-300"
                  >Your password</label
                >
                <input
                  type="password"
                  name="password"
                  id="password"
                  placeholder="••••••••"
                  class="bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-600 dark:border-gray-500 dark:placeholder-gray-400 dark:text-white"
                  required=""
                />
              </div>
              <div class="flex justify-between">
                <div class="flex items-start">
                  <div class="flex items-center h-5">
                    <input
                      id="remember"
                      aria-describedby="remember"
                      type="checkbox"
                      class="bg-gray-50 border border-gray-300 focus:ring-3 focus:ring-blue-300 h-4 w-4 rounded dark:bg-gray-600 dark:border-gray-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800"
                      required=""
                    />
                  </div>
                  <div class="text-sm ml-3">
                    <label
                      for="remember"
                      class="font-medium text-gray-900 dark:text-gray-300"
                      >Remember me</label
                    >
                  </div>
                </div>
                <a
                  href="#"
                  class="text-sm text-blue-700 hover:underline dark:text-blue-500"
                  >Lost Password?</a
                >
              </div>
              <button
                type="submit"
                class="w-full text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800"
              >
                Login to your account
              </button>
              <div class="text-sm font-medium text-gray-500 dark:text-gray-300">
                Not registered?
                <a
                  href="#"
                  class="text-blue-700 hover:underline dark:text-blue-500"
                  >Create account</a
                >
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>

    <div class="flex items-center flex-nowrap pl-8 text-grey">
      <svg
        xmlns="http://www.w3.org/2000/svg"
        fill="none"
        viewBox="0 0 24 24"
        stroke-width="1.5"
        stroke="currentColor"
        class="w-4 h-4"
      >
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          d="M12 6v6h4.5m4.5 0a9 9 0 11-18 0 9 9 0 0118 0z"
        />
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
      <p class="text-bold">Description</p>
      <p class="pr-8">{{ description }}</p>
    </div>

    <div class="mt-1 p-10">
      <p class="text-bold">Required Skills</p>
      <ul class="list-disc pl-4">
        <li v-for="skill in skills" :key="skill">{{ skill }}</li>
      </ul>
    </div>
  </div>
</template>

<link rel="stylesheet" href="https://unpkg.com/@themesberg/flowbite@1.2.0/dist/flowbite.min.css" />


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
    openApply() {
      document.getElementById('authentication-modal').classList.remove('hidden')
    },
    closeApply() {
      document.getElementById('authentication-modal').classList.add('hidden')
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