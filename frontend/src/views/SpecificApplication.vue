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

    <div class="grid grid-cols-3 mt-10 px-10">
      <div>
        <p class="font-bold">Email</p>
        <p id="email">{{ staffDetails.email }}</p>
      </div>
      <div class="mx-auto">
        <p class="font-bold">Hiring Department</p>
        <p id="hiring-department">{{ staffDetails.dept }}</p>
      </div>
      <div class="ml-auto">
        <p class="font-bold">Country</p>
        <p id="country">{{ staffDetails.country }}</p>
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
  roles,
  staff,
  roleSkills,
  staffSkills,
  backend_url,
} = storeToRefs(store);

const applicationStore = useApplicationStore();
const applicantID = applicationStore.staffId

const roleName = ref("");
var department = ref("");
const applications = ref([]);
var specificApplication = ref([]);
const staffDetails = ref({});

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
    console.log(staffDetails.value);

  }
  catch (error) {
    console.log(error.message);
  }
})

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