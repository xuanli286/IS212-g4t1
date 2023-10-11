<script>
import axios from "axios";
import { storeToRefs } from "pinia";
import { ref } from "vue"; // Import ref from Vue
import { useUserStore } from "../store/useUserStore";
import { useConstantStore } from "../store/useConstantStore";

const rolelistingID = 1;

export default {
  name: "SpecificRoleListing",
  components: {},
  props: {},
  setup() {
    const backend_url = useConstantStore().backend_url;

    const user = useUserStore().user;
    const currentUser = ref(user);

    return { backend_url, currentUser };
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
      hrRights: false,
      staffSkills: [],
    };
  },
  methods: {
    getRoleListingInfo() {
      axios
        .get(`${this.backend_url}/rolelisting/${rolelistingID}`)
        .then((response) => {
          // console.log(response.data.data[rolelistingID])
          this.roleName = response.data.data[rolelistingID]["role_name"];
          this.expiryDate =
            response.data.data[rolelistingID]["application_deadline"];
          this.managerId = response.data.data[rolelistingID]["manager_ID"];
          this.department = response.data.data[rolelistingID]["dept"];
          this.country = response.data.data[rolelistingID]["country"];

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
        .get(`${this.backend_url}/staff/${this.managerId}`)
        .then((response) => {
          const managerData = response.data.data[this.managerId];
          if (managerData) {
            this.managerName =
              managerData["staff_FName"] + " " + managerData["staff_LName"];
          }
        })
        .catch((error) => {
          console.log(error.message);
        });
    },
    getRoleSkills() {
      axios
        .get(`${this.backend_url}/get_role_skill/${this.roleName}`)
        .then((response) => {
          const roleSkillsData = response.data.data;
          console.log(roleSkillsData);
          if (roleSkillsData) {
            this.skills = roleSkillsData;
          }
        })
        .catch((error) => {
          console.log(error.message);
        });
    },
    openApply() {
      document
        .getElementById("authentication-modal")
        .classList.remove("hidden");
      console.log(this.currentUser);
      console.log(this.currentUser.access_ID);
      console.log(this.staffSkills);
    },
    closeApply() {
      document.getElementById("authentication-modal").classList.add("hidden");
    },
    getRoleDescription() {
      axios
        .get(`${this.backend_url}/get_all_role`)
        .then((response) => {
          const roleDescriptionsData = response.data.data;
          for (const role of roleDescriptionsData) {
            for (let rName in role) {
              if (rName == this.roleName) {
                this.description = role[this.roleName];
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
    },
    submitApplication() {
      console.log("Hello");
    //   axios
    //     .post(`${this.backend_url}/apply_role`, {
    //       staff_ID: this.currentUser.staff_ID,
    //       role_name: this.roleName,
    //     })
    //     .then((response) => {
    //       console.log(response);
    //     })
    //     .catch((error) => {
    //       console.log(error.message);
    //     });
    //   document
    //     .getElementById("confirm-modal")
    //     .classList.remove("hidden");
    // },
    closeConfirm() {
      document.getElementById("confirm-modal").classList.add("hidden");
    },
  },
  created() {
    this.getRoleListingInfo();
    if (this.currentUser.access_ID == 2) {
      this.hrRights = true;
    }
    axios
      .get(`${this.backend_url}/get_staff_skill/${this.currentUser.staff_ID}`)
      .then((response) => {
        this.staffSkills = response.data.data;
      })
      .catch((error) => {
        console.log(error.message);
      });
  },
};
</script>

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
        v-if="hrRights"
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
        class="inset-y-0 inset-x-0 hidden overflow-x-hidden overflow-y-auto bg-grey bg-opacity-75 fixed h-modal md:h-full top-4 left-0 right-0 md:inset-0 z-50 flex items-center justify-center"
      >
        >
        <div class="relative pt-6 h-full w-11/12 md:h-auto w">
          <!-- Modal content -->
          <div class="bg-white p-4 pb-0 rounded-lg shadow relative">
            <div class="bg-yellow w-full py-2 rounded-lg text-center">
              <span class="text-white text-lg">Confirm Details</span>
            </div>
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
            <div class="flex items-center justify-center -mt-6">
              <span class="font-serif text-lg">Apply Role</span>
            </div>
            <!-- form div here -->
            <div
              class="space-y-6 px-6 lg:px-8 pb-4 sm:pb-6 xl:pb-8 my-3"
              action="#"
            >
              <div class="bg-grey-50 px-4 py-6 md:px-8 my-3">
                <div class="grid grid-cols-3 pt-5 gap-6 md:gap-8">
                  <div>
                    <span class="font-bold pr-3">Staff ID:</span>
                    <input
                      type="text"
                      class="mt-1 p-2 bg-grey-20 border-2 text-grey border-yellow rounded-md w-40"
                      :value="this.currentUser.staff_ID"
                      placeholder="1389503"
                      disabled
                    />
                  </div>
                  <div>
                    <span class="font-bold pr-3">Department:</span>
                    <input
                      type="text"
                      class="mt-1 p-2 bg-grey-20 text-grey border-2 border-yellow rounded-md w-64"
                      :value="this.currentUser.staff_dept"
                      placeholder="IT"
                      disabled
                    />
                  </div>
                  <div></div>
                </div>
                <!-- Second row of inputs -->
                <div class="grid grid-cols-3 pt-5 gap-6">
                  <div>
                    <span class="font-bold pr-3">First Name:</span>
                    <input
                      type="text"
                      class="mt-1 p-2 bg-grey-20 text-grey border-2 border-yellow rounded-md"
                      :value="this.currentUser.staff_FName"
                      disabled
                    />
                  </div>
                  <div>
                    <span class="font-bold pr-3">Last Name:</span>
                    <input
                      type="text"
                      class="mt-1 p-2 bg-grey-20 text-grey border-2 border-yellow rounded-md"
                      :value="this.currentUser.staff_LName"
                      placeholder="Tam"
                      disabled
                    />
                  </div>
                  <div>
                    <span class="font-bold pr-3">Email:</span>
                    <input
                      type="text"
                      class="mt-1 p-2 bg-grey-20 text-grey border-2 border-yellow rounded-md"
                      :value="this.currentUser.staff_email"
                      placeholder="email@123.com"
                      disabled
                    />
                  </div>
                </div>
                <!-- Third row of inputs  -->
                <div class="grid grid-cols-1 pt-5 gap-6 md:gap-8">
                  <span class="font-bold">Your Skills</span>
                  <div class="flex flex-col gap-2">
                    <label v-for="(skill, index) in staffSkills" :key="index">
                      <input
                        type="checkbox"
                        :name="skill"
                        :id="skill"
                        v-model="selectedSkills"
                        :value="skill"
                        disabled
                        checked
                      />
                      {{ skill }}
                    </label>
                  </div>
                </div>
              </div>
              <div class="flex justify-end">
                <button
                  @click="goBack"
                  class="text-white bg-grey border-0 py-2 px-6 focus:outline-none hover:bg-yellow-600 rounded-md text-md mr-3"
                >
                  Cancel
                </button>
                <button
                  @click="submitApplication"
                  class="text-white bg-yellow border-0 py-2 px-6 focus:outline-none hover:bg-yellow-600 rounded-md text-md"
                >
                  Submit
                </button>
                <div
                  id="confirm-modal"
                  tabindex="-1"
                  class="fixed top-0 left-0 right-0 z-50 bg-grey bg-opacity-75 hidden w-full p-4 overflow-x-hidden overflow-y-auto md:inset-0 h-[calc(100%-1rem)] max-h-full justify-center flex pt-24"
                >
                  <div class="relative w-full max-w-md max-h-full">
                    <!-- Modal content -->
                    <div
                      class="relative text-center bg-white rounded-lg shadow dark:bg-gray-700 w-full"
                    >
                      <!-- Modal header -->
                      <div
                        class="relative flex flex-col items-center justify-between rounded-t dark:border-gray-600 text-center"
                      >
                        <button
                          type="button"
                          class="text-gray-400 bg-transparent hover:bg-gray-200 hover:text-gray-900 rounded-lg text-sm w-8 h-8 ml-auto inline-flex justify-center items-center dark:hover:bg-gray-600 dark:hover:text-white"
                          @click="closeConfirm"
                        >
                          <svg
                            class="w-3 h-3"
                            aria-hidden="true"
                            xmlns="http://www.w3.org/2000/svg"
                            fill="none"
                            viewBox="0 0 14 14"
                          >
                            <path
                              stroke="currentColor"
                              stroke-linecap="round"
                              stroke-linejoin="round"
                              stroke-width="2"
                              d="m1 1 6 6m0 0 6 6M7 7l6-6M7 7l-6 6"
                            />
                          </svg>
                        </button>
                        <span class="text-green relative font-serif text-lg"
                          >Role Applied Successfully!</span
                        >
                      </div>
                      <!-- Modal body -->
                      <div
                        class="p-6 space-y-6 flex flex-col justify-center items-center h-full"
                      >
                        <p
                          class="text-base leading-relaxed text-gray-500 dark:text-gray-400"
                        >
                          Thank you for your interest in the role!
                        </p>
                        <p
                          class="text-base leading-relaxed text-gray-500 dark:text-gray-400"
                        >
                          Your application is currently under review. <br />
                          We appreciate your patience and will be in touch soon.
                        </p>
                      </div>
                      <!-- Modal footer -->
                      <div
                        class="flex items-center space-x-2 border-gray-200 rounded-b dark:border-gray-600"
                      ></div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
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