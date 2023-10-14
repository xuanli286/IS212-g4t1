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
      <Button id="edit" class="ml-auto" @click="editRole">
        <template v-slot:icon>
          <img class="mr-1" src="@/assets/icons/edit.svg" alt="">
        </template>
        <template v-slot:text>
          Edit Role Listing
        </template>
      </Button>
    </div>
    <div class="grid grid-cols-3 mt-10">
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
    <div class="grid grid-cols-2 gap-20 mt-10">
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

const store = useConstantStore();
const {
  roles,
  staff,
  roleSkills,
  backend_url,
} = storeToRefs(store);

const roleName = ref("");
const roleDetails = ref({});

const rolelistingID = route.params.id;

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

function back() {
  window.history.back();
}

function editRole() {
  router.push(`/editrolelisting/${rolelistingID}`);
}
</script>