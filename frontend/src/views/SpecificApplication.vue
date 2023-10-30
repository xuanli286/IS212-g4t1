<template>
  <div class="bg-beige px-10 py-7">
    <div class="flex items-center">
      <div>
        <div class="flex items-center">
          <img id="back" src="@/assets/icons/back.svg" alt="" @click=back()>
          <p class="font-light text-2xl text-yellow ml-4" id="role-name">{{ roleName }}</p>
        </div>
        <div class="flex flex-col ml-8">
          <div class="mb-1">
            <p>Department: {{ department }}</p>
          </div>
          <div class="flex items-center">
            <img src="@/assets/icons/clock.svg" alt="">
            <p id="application-deadline" class="ml-1 text-grey text-sm">
              <span class="font-bold">Applied On:</span>
              <span class="font-light ml-1">{{ formatDate(specificApplication["application_date"]) }}</span>
            </p>
          </div>
        </div>
      </div>
    </div>

    <div class="grid grid-rows-2 grid-cols-3 mt-10 px-10 gap-y-10">
      <div>
        <p class="font-bold text-yellow">Full Name</p>
        <p id="name">{{ staffDetails.staff_FName }} {{ staffDetails.staff_LName }}</p>
      </div>
      <div>
        <p class="font-bold text-yellow">Staff ID</p>
        <p id="id">{{ applicantID }}</p>
      </div>
      <div>
        <p class="font-bold text-yellow">Skill Match</p>
        <p id="percentageMatch">{{ specificApplication.percentage_match }}%</p>
      </div>
      <div>
        <p class="font-bold text-yellow">Email</p>
        <p id="email">{{ staffDetails.email }}</p>
      </div>
      <div>
        <p class="font-bold text-yellow">Department</p>
        <p id="hiring-department">{{ staffDetails.dept }}</p>
      </div>
      <div>
        <p class="font-bold text-yellow">Country</p>
        <p id="country">{{ staffDetails.country }}</p>
      </div>
    </div>

    <div class="mx-10 mt-10 rounded-lg bg-white p-5">
      <div class="flex items-center">
        <img src="@/assets/icons/puzzle.svg" alt="">
        <p class="font-bold text-yellow ml-1">Skills Match</p>
      </div>
      <div class="ml-8">
        <p class="mt-2 font-serif text-green text-sm" id="">{{ matchedSkills.length }}/{{ roleSkills.length }}
          skills
          matched</p>
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
import { useApplicationStore } from '@/store/useApplicationStore';
import { useUserStore } from "@/store/useUserStore";
import { storeToRefs } from 'pinia';
import { useRoute } from 'vue-router';
import axios from "axios";
import router from "@/router";

const route = useRoute();

const userStore = useUserStore();
const {
  user,
} = storeToRefs(userStore);

const store = useConstantStore();
const {
  backend_url,
} = storeToRefs(store);

const applicationStore = useApplicationStore();
const applicantID = applicationStore.staffId

const roleName = ref("");
var department = ref("");
const applications = ref([]);
var specificApplication = ref([]);
const staffDetails = ref({});
const staffSkills = ref([]);
const roleSkills = ref([]);

const rolelistingID = route.params.id;

onMounted(async () => {
  try {
    const response = await axios.get(`${backend_url.value}/applications/${rolelistingID}`);
    applications.value = response.data.data;

    // get specific application
    for (let i = 0; i < applications.value.length; i++) {
      if (applications.value[i].staff_ID === applicantID) {
        specificApplication = applications.value[i];
        break;
      }
    }

    // get role name
    const response_rolename = await axios.get(`${backend_url.value}/rolelisting/${rolelistingID}`);
    roleName.value = response_rolename.data.data[rolelistingID]["role_name"];

    // get department
    const response_dept = await axios.get(`${backend_url.value}/rolelisting/${rolelistingID}`);
    department.value = response_rolename.data.data[rolelistingID]["dept"];

    // get staff details
    const response_staff = await axios.get(`${backend_url.value}/staff/${applicantID}`);
    staffDetails.value = response_staff.data.data[applicantID];

    // get staff skills
    const response_staffskills = await axios.get(`${backend_url.value}/get_staff_skill/${applicantID}`);
    staffSkills.value = response_staffskills.data.data;

    // get role skills
    const response_roleskills = await axios.get(`${backend_url.value}/get_role_skill/${roleName.value}`);
    roleSkills.value = response_roleskills.data.data;

  }
  catch (error) {
    console.log(error.message);
  }
})

// skills handling
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

function formatDate(dateString) {
  const date = new Date(dateString);
  const day = date.getDate();
  const month = date.toLocaleString('default', { month: 'long' });
  const year = date.getFullYear();
  return `${day} ${month} ${year}`;
}

function back() {
  window.history.back();
}
</script>