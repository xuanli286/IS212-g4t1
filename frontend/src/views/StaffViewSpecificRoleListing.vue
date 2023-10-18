<template>
  <div class="bg-beige px-10 py-7">
    <div class="flex items-center">
      <div>
        <div class="flex items-center">
          <img id="back" src="@/assets/icons/back.svg" alt="" @click=back()>
          <p class="font-light text-2xl text-yellow ml-4" id="role-name">{{ roleName }}</p>
        </div>
        <div class="flex items-center ml-8">
          <img src="@/assets/icons/clock.svg" alt="">
          <p id="application-deadline" class="ml-1 text-grey text-sm">
            <span class="font-bold">Expires On:</span>
            <span class="font-light ml-1">{{ new Date(roleDetails.application_deadline).toLocaleDateString('en-US', {
              day:
                'numeric', month: 'long', year: 'numeric'
            }) }}</span>
          </p>
        </div>
      </div>
      <Button id="apply" class="ml-auto" @click="openApply">
        <template v-slot:icon>
          <img class="mr-1" src="@/assets/icons/attachdocument.svg" alt="">
        </template>
        <template v-slot:text>
          Apply Role
        </template>
      </Button>
      <!-- Main modal -->
      <div id="authentication-modal" aria-hidden="true"
        class="inset-y-0 inset-x-0 hidden overflow-x-hidden overflow-y-auto bg-grey bg-opacity-75 fixed h-modal md:h-full top-4 left-0 right-0 md:inset-0 z-50 flex items-center justify-center">
        >
        <div class="relative pt-6 h-full w-11/12 md:h-auto w">
          <!-- Modal content -->
          <div class="bg-white p-4 pb-0 rounded-lg shadow relative">
            <div class="bg-yellow w-full py-2 rounded-lg text-center">
              <span class="text-white text-lg">Confirm Details</span>
            </div>
            <div class="flex justify-end p-2">
              <button type="button"
                class="text-gray-400 bg-transparent hover:bg-gray-200 hover:text-gray-900 rounded-lg text-sm p-1.5 ml-auto inline-flex items-center dark:hover:bg-gray-800 dark:hover:text-white"
                @click="closeApply">
                <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
                  <path fill-rule="evenodd"
                    d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
                    clip-rule="evenodd"></path>
                </svg>
              </button>
            </div>
            <div class="flex items-center justify-center -mt-6">
              <span class="font-serif text-lg">Apply Role</span>
            </div>
            <!-- form div here -->
            <div class="space-y-6 px-6 lg:px-8 pb-4 sm:pb-6 xl:pb-8 my-3" action="#">
              <div class="bg-grey-50 px-4 py-6 md:px-8 my-3">
                <div class="grid grid-cols-3 pt-5 gap-6 md:gap-8">
                  <div>
                    <span class="font-bold pr-3">Staff ID:</span>
                    <input type="text" class="mt-1 p-2 bg-grey-20 border-2 text-grey border-yellow rounded-md w-40"
                      :value="user['staff_ID']" disabled />
                  </div>
                  <div>
                    <span class="font-bold pr-3">Department:</span>
                    <input type="text" class="mt-1 p-2 bg-grey-20 text-grey border-2 border-yellow rounded-md w-64"
                      :value="user['staff_dept']" placeholder="IT" disabled />
                  </div>
                  <div></div>
                </div>
                <!-- Second row of inputs -->
                <div class="grid grid-cols-3 pt-5 gap-6">
                  <div>
                    <span class="font-bold pr-3">First Name:</span>
                    <input type="text" class="mt-1 p-2 bg-grey-20 text-grey border-2 border-yellow rounded-md"
                      :value="user['staff_FName']" disabled />
                  </div>
                  <div>
                    <span class="font-bold pr-3">Last Name:</span>
                    <input type="text" class="mt-1 p-2 bg-grey-20 text-grey border-2 border-yellow rounded-md"
                      :value="user['staff_LName']" placeholder="Tam" disabled />
                  </div>
                  <div>
                    <span class="font-bold pr-3">Email:</span>
                    <input type="text" class="mt-1 p-2 bg-grey-20 text-grey border-2 border-yellow rounded-md"
                      :value="user['staff_email']" placeholder="email@123.com" disabled />
                  </div>
                </div>
                <!-- Third row of inputs  -->
                <div class="grid grid-cols-1 pt-5 gap-6 md:gap-8">
                  <span class="font-bold">Your Skills</span>
                  <div class="flex flex-col gap-2">
                    <label v-for="(skill, index) in staffSkills" :key="index">
                      <input type="checkbox" :name="skill" :id="skill" v-model="selectedSkills" :value="skill" disabled
                        checked />
                      {{ skill }}
                    </label>
                  </div>
                </div>
              </div>
              <div class="flex justify-end">
                <button @click="goBack"
                  class="text-white bg-grey border-0 py-2 px-6 focus:outline-none hover:bg-yellow-600 rounded-md text-md mr-3">
                  Cancel
                </button>
                <button @click="submitApplication"
                  class="text-white bg-yellow border-0 py-2 px-6 focus:outline-none hover:bg-yellow-600 rounded-md text-md">
                  Submit
                </button>
                <div id="confirm-modal" tabindex="-1"
                  class="fixed top-0 left-0 right-0 z-50 bg-grey bg-opacity-75 hidden w-full p-4 overflow-x-hidden overflow-y-auto md:inset-0 h-[calc(100%-1rem)] max-h-full justify-center flex pt-24">
                  <div class="relative w-full max-w-md max-h-full">
                    <!-- Modal content -->
                    <div class="relative text-center bg-white rounded-lg shadow dark:bg-gray-700 w-full">
                      <!-- Modal header -->
                      <div
                        class="relative flex flex-col items-center justify-between rounded-t dark:border-gray-600 text-center">
                        <button type="button"
                          class="text-gray-400 bg-transparent hover:bg-gray-200 hover:text-gray-900 rounded-lg text-sm w-8 h-8 ml-auto inline-flex justify-center items-center dark:hover:bg-gray-600 dark:hover:text-white"
                          @click="closeConfirm">
                          <svg class="w-3 h-3" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none"
                            viewBox="0 0 14 14">
                            <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                              d="m1 1 6 6m0 0 6 6M7 7l6-6M7 7l-6 6" />
                          </svg>
                        </button>
                        <span v-if="applicationSuccess" class="text-green relative font-serif text-lg">Role Applied
                          Successfully!</span>
                        <span v-else class="text-red relative font-serif text-lg">Application Unsuccessful</span>
                      </div>
                      <!-- Modal body -->
                      <div class="p-6 space-y-6 flex flex-col justify-center items-center h-full">
                        <p class="text-base leading-relaxed text-gray-500 dark:text-gray-400">
                          Thank you for your interest in the role!
                        </p>
                        <p v-if="applicationSuccess" class="text-base leading-relaxed text-gray-500 dark:text-gray-400">
                          Your application is currently under review. <br />
                          We appreciate your patience and will be in touch soon.
                        </p>
                        <p v-else class="text-base leading-relaxed text-gray-500 dark:text-gray-400">
                          There was an error with your application. You may only apply for a role once. If you think this
                          is an error, please contact the Human Resource team.
                        </p>
                      </div>
                      <!-- Modal footer -->
                      <div class="flex items-center space-x-2 border-gray-200 rounded-b dark:border-gray-600"></div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="mx-10 grid grid-cols-3 mt-10">
      <div>
        <p class="font-bold">Reporting Manager</p>
        <p id="manager">{{ staff[roleDetails.manager_ID] }}</p>
      </div>
      <div class="mx-auto">
        <p class="font-bold">Hiring Department</p>
        <p id="hiring-department">{{ roleDetails.dept }}</p>
      </div>
      <div class="ml-auto">
        <p class="font-bold">Country</p>
        <p id="country">{{ roleDetails.country }}</p>
      </div>
    </div>
    <div class="mx-10 grid grid-cols-2 gap-20 mt-10">
      <div>
        <p class="font-bold">Description</p>
        <p class="text-justify" id="role-description">{{ roles[roleName] }}</p>
      </div>
      <div>
        <p class="font-bold">Required Skills</p>
        <ul id="required-skills" class="list-disc ml-6" v-for="skill of roleSkills" :key="skill">
          <li>
            {{ skill }}
          </li>
        </ul>
      </div>
    </div>
    <div class="mx-10 mt-10 rounded-lg bg-white p-5">
      <div class="flex items-center">
        <img src="@/assets/icons/puzzle.svg" alt="">
        <p class="font-bold text-yellow ml-1">Skills Match</p>
      </div>
      <div class="ml-8">
        <p class="mt-2 font-serif text-green text-sm" id="percentage">{{
          (matchedSkills.length / roleSkills.length * 100).toFixed(0) }}% skills match</p>
        <div class="flex gap-1">
          <img v-for="skill of matchedSkills.length" :key="skill" src="@/assets/matchedSkill.svg" alt="">
          <img v-for="skill of missingSkills.length" :key="skill" src="@/assets/unmatchedSkill.svg" alt="">
        </div>
        <div class="mt-2">
          <div class="flex items-center">
            <img src="@/assets/icons/check.svg" alt="">
            <p class="font-bold text-sm ml-1">{{ matchedSkills.length }} skills on your profile</p>
          </div>
          <p class="ml-4 text-sm" id="matched-skills">
            <span v-if="matchedSkills.length > 0">{{ matchedSkills.join(', ') }}</span>
            <span v-else class="text-grey">No matching skill found</span>
          </p>
        </div>
        <div class="mt-2">
          <div class="flex items-center">
            <img src="@/assets/icons/exclamation.svg" alt="">
            <p class="font-bold text-sm ml-1">{{ missingSkills.length }} skills missing on your profile</p>
          </div>
          <p class="ml-4 text-sm" id="missing-skills">
            <span v-if="missingSkills.length > 0">{{ missingSkills.join(', ') }}</span>
            <span v-else class="text-grey">All skills matched</span>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { useConstantStore } from "@/store/useConstantStore";
import { useUserStore } from "@/store/useUserStore";
import { storeToRefs } from 'pinia';
import { useRoute } from 'vue-router';
import axios from "axios";
import Button from "@/components/Button.vue";
import router from "@/router";

const route = useRoute();

const userStore = useUserStore();
const {
  user,
} = storeToRefs(userStore);
console.log(user.value.staff_ID)

const store = useConstantStore();
const {
  roles,
  staff,
  roleSkills,
  staffSkills,
  backend_url,
} = storeToRefs(store);

const rolelistingID = route.params.id;

const roleName = ref("");
const roleDetails = ref({});
var applicationSuccess = ref(false);

onMounted(async () => {
  try {
    const response = await axios.get(`${backend_url.value}/rolelisting/${rolelistingID}`);
    roleDetails.value = response.data.data[rolelistingID];
    roleName.value = roleDetails.value.role_name;
    store.getSkills(roleName.value);
    store.getStaffSkills(user.value.staff_ID);
  }
  catch (error) {
    console.log(error.message);
  }
})

const matchedSkills = computed(() => {
  const matched = [];
  for (let skill of roleSkills.value) {
    if (staffSkills.value.indexOf(skill) !== -1) {
      matched.push(skill);
    }
  }
  return matched;
});

const missingSkills = computed(() => {
  const missing = [];
  for (let skill of roleSkills.value) {
    if (staffSkills.value.indexOf(skill) === -1) {
      missing.push(skill);
    }
  }
  return missing;
});

function back() {
  window.history.back();
}

function openApply() {
  document
    .getElementById("authentication-modal")
    .classList.remove("hidden");
  //   console.log(this.currentUser);
  //   console.log(this.currentUser.access_ID);
  //   console.log(this.staffSkills);
}

function closeApply() {
  document.getElementById("authentication-modal").classList.add("hidden");
}

function submitApplication() {
  console.log("Hello");
  const body = {
    staff_ID: user.value.staff_ID,
    rolelisting_ID: rolelistingID,
    application_date: new Date().toISOString().slice(0, 10),
    percentage_match: getSkillPercentage(),
  };
  console.log(body);
  axios
    .post(`${backend_url.value}/addapplication`, body)
    .then((response) => {
      console.log(response);
      applicationSuccess.value = true;
    })
    .catch((error) => {
      console.log(error.message);
      applicationSuccess.value = false;
    });

  document.getElementById("confirm-modal").classList.remove("hidden");
}

function closeConfirm() {
  document.getElementById("confirm-modal").classList.add("hidden");
}

function getSkillPercentage() {
  return (matchedSkills.value.length / roleSkills.value.length) * 100;
}
</script>