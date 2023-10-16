<template>
  <div>
    <div class="mx-64 py-20">
      <img id="back" src="@/assets/icons/back.svg" alt="" @click=back()>
      <h1 class="text-xl font-serif text-center">Applicants</h1>
    </div>

    <ul class="mx-64 min-w-fit applications-container">
      <li v-if="Object.keys(applications).length == 0" class="py-5 text-center">
        <div class="grow"></div>
        <div class="font-bold">No applications available!</div>
        <div class="grow"></div>
      </li>
      <li v-else v-for="(application, index) in applications" :key="index"
        class="applicants-panel flex border-t py-5 hover:bg-grey-50">
        <p>{{ application.staff_ID }}</p>
      </li>
    </ul>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { useConstantStore } from "@/store/useConstantStore";
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


function back() {
  window.history.back();
}
</script>