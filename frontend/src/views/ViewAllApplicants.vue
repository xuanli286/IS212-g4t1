<template>
  <div>
    <div class="mx-64 py-20">
      <img id="back" src="@/assets/icons/back.svg" class="cursor-pointer" @click=back()>
      <h1 v-if="Object.keys(applications).length == 0" class="text-xl font-serif text-center">Applications</h1>
      <h1 v-else class="text-xl font-serif text-center">Applications for {{ roleName }} ({{ department }})</h1>
    </div>

    <ul class="mx-64 min-w-fit applications-container">
      <li v-if="Object.keys(applications).length == 0" class="py-5 text-center">
        <div class="grow"></div>
        <div class="font-bold">No applications available!</div>
        <div class="grow"></div>
      </li>
      <li v-else v-for="(application, index) in applications" :key="index"
        class="applicants-panel flex border-t py-5 hover:bg-grey-50 justify-between"
        @click="viewApplication(application.staff_ID)">

        <div class="flex-none h-100">
          <div class="role-title text-yellow text-xl"> {{ staff[application.staff_ID] }} </div>
          <div class="flex flex-col text-xs">
            <div class=""> Staff ID: {{ application.staff_ID }}</div>
            <div class="role-deadline text-grey"> Applied on {{ formatDate(application.application_date) }}</div>
          </div>
        </div>
        <div class="text-center">
          <div class="text-xs">Skill Match</div>
          <div :class="application.percentage_match >= 70 ? 'text-green' : 'text-red'">
            {{ application.percentage_match }}%
          </div>
        </div>
      </li>
    </ul>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useConstantStore } from "@/store/useConstantStore";
import { useApplicationStore } from '@/store/useApplicationStore';
import { storeToRefs } from 'pinia';
import { useRoute } from 'vue-router';
import axios from "axios";
import router from "@/router";

const route = useRoute();

const applicationStore = useApplicationStore();

const store = useConstantStore();
const {
  backend_url,
  staff
} = storeToRefs(store);

const applications = ref({});
const rolelistingID = route.params.id;
var roleName = ref("");
var department = ref("");

onMounted(async () => {
  try {
    const response = await axios.get(`${backend_url.value}/applications/${rolelistingID}`);
    applications.value = response.data.data;

    // get role name
    const response_rolename = await axios.get(`${backend_url.value}/rolelisting/${rolelistingID}`);
    roleName.value = response_rolename.data.data[rolelistingID]["role_name"];

    // get department
    const response_dept = await axios.get(`${backend_url.value}/rolelisting/${rolelistingID}`);
    department.value = response_rolename.data.data[rolelistingID]["dept"];
  }
  catch (error) {
    console.log(error.message);
  }
})

function viewApplication(staffId) {
  applicationStore.setStaffId(staffId);
  router.push('/application/' + rolelistingID);
}

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