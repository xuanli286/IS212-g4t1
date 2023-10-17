<template>
  <div>
    <div class="mx-64 py-20">
      <img id="back" src="@/assets/icons/back.svg" class="cursor-pointer" @click=back()>
      <h1 class="text-xl font-serif text-center">Applicants</h1>
    </div>

    <ul class="mx-64 min-w-fit applications-container">
      <li v-if="Object.keys(applications).length == 0" class="py-5 text-center">
        <div class="grow"></div>
        <div class="font-bold">No applications available!</div>
        <div class="grow"></div>
      </li>
      <li v-else v-for="(application, index) in applications" :key="index"
        class="applicants-panel flex border-t py-5 hover:bg-grey-50 justify-between">

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
import { storeToRefs } from 'pinia';
import { useRoute } from 'vue-router';
import axios from "axios";

const route = useRoute();

const store = useConstantStore();
const {
  backend_url,
  staff
} = storeToRefs(store);

const applications = ref({});
const rolelistingID = route.params.id;

onMounted(async () => {
  try {
    const response = await axios.get(`${backend_url.value}/applications/${rolelistingID}`);
    applications.value = response.data.data;
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