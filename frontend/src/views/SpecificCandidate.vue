<template>
  <div class="bg-beige px-10 py-7">
    <div class="flex items-center">
      <div>
        <div class="flex items-center">
          <img id="back" src="@/assets/icons/back.svg" alt="" @click=back()>
          <p class="font-light text-2xl text-yellow ml-4" id="name">{{ staffDetails.staff_FName }} {{
            staffDetails.staff_LName }}</p>
        </div>
        <div class="flex flex-col ml-8">
          <div class="mb-1">
            <p id="department">{{ staffDetails.dept }}</p>
          </div>
        </div>
      </div>
    </div>

    <div class="grid grid-cols-3 mt-10 px-10 gap-y-10">
      <div>
        <p class="font-bold text-yellow">Email</p>
        <p id="email">{{ staffDetails.email }}</p>
      </div>
      <div>
        <p class="font-bold text-yellow">Staff ID</p>
        <p id="staffID">{{ staffID }}</p>
      </div>
      <div>
        <p class="font-bold text-yellow">Country</p>
        <p id="country">{{ staffDetails.country }}</p>
      </div>
    </div>

    <div class="mt-10 px-10">
      <p class="font-bold text-yellow">Staff Skills</p>
      <ul id="staff-skills" class="list-disc ml-6" v-if="staffSkills.length > 0">
        <li v-for="skill of staffSkills" :key="skill">
          {{ skill }}
        </li>
      </ul>
      <p v-else id="no-skills">No skills found in database</p>
    </div>

  </div>
</template>


<script setup>
import { ref, onMounted } from "vue";
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

const staffDetails = ref({});
const staffSkills = ref([]);

const staffID = route.params.id;

onMounted(async () => {
  try {
    const response_staff = await axios.get(`${backend_url.value}/staff/${staffID}`);
    staffDetails.value = response_staff.data.data[staffID];

    // get staff skills
    const response_staffskills = await axios.get(`${backend_url.value}/get_staff_skill/${staffID}`);
    staffSkills.value = response_staffskills.data.data;
  }
  catch (error) {
    console.log(error.message);
  }
})

function back() {
  window.history.back();
}
</script>