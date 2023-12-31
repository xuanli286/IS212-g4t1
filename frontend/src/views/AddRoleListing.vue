<script setup>
import axios from "axios";
import Button from "@/components/Button.vue";
import Modal from "@/components/Modal.vue";
import { ref, computed } from "vue";
import { storeToRefs } from "pinia";
import { useConstantStore } from "@/store/useConstantStore";
import { useModalStore } from "@/store/useModalStore";
import { useUserStore } from "@/store/useUserStore";

const store = useModalStore();
const { isOpen, isSuccess } = storeToRefs(store);

const constStore = useConstantStore();
const { hiringDepartment, countries, staff, backend_url } = storeToRefs(constStore);

const userStore = useUserStore();
const { user } = storeToRefs(userStore);

// const rolelistingID = 3;

const roles = ref({});
const selectedTitle = ref("");
const applicationOpening = ref("");
const applicationDeadline = ref("");
const selectedDept = ref("");
const selectedCountry = ref("");
const skills = ref([]);
const managerID = ref([]);
const errorMessage = ref("");
const roleListingId = ref("")

const today = new Date();

const minOpenDate = computed(() => {
  let year = today.getFullYear();
  let month = String(today.getMonth() + 1).padStart(2, "0");
  let day = String(today.getDate()).padStart(2, "0");
  return `${year}-${month}-${day}`;
});

applicationOpening.value = minOpenDate.value;

const minCloseDate = computed(() => {
  const dates = [new Date(applicationOpening.value), today];
  const maxDate = new Date(Math.max.apply(null, dates));
  maxDate.setDate(maxDate.getDate() + 1);
  const year = maxDate.getFullYear();
  const month = String(maxDate.getMonth() + 1).padStart(2, "0");
  const day = String(maxDate.getDate()).padStart(2, "0");
  return `${year}-${month}-${day}`;
});

function updateMinCloseDate() {
  const dates = [new Date(applicationOpening.value), today];
  const maxDate = new Date(Math.max.apply(null, dates));
  maxDate.setDate(maxDate.getDate() + 1);
  let year = maxDate.getFullYear();
  let month = String(maxDate.getMonth() + 1).padStart(2, "0");
  let day = String(maxDate.getDate()).padStart(2, "0");
  minCloseDate.value = `${year}-${month}-${day}`;
  applicationDeadline.value = minCloseDate.value;
}

function validateApplicationOpening() {
  const enteredDate = new Date(applicationOpening.value);
  const minDate = new Date(minOpenDate.value);
  if (enteredDate < minDate) {
    applicationOpening.value = minOpenDate.value;
  }
}

function validateApplicationDeadline() {
  const enteredDate = new Date(applicationDeadline.value);
  const minDate = new Date(minCloseDate.value);
  if (enteredDate < minDate) {
    applicationDeadline.value = minCloseDate.value;
  }
}

axios
  .get(`${backend_url.value}/get_all_role`)
  .then((response) => {
    for (let i of response.data.data) {
      for (let key in i) {
        roles.value[key] = i[key];
      }
    }
  })
  .catch((error) => {
    console.log(error.message);
  });

function addRoleListing() {
  if (user.value.access_ID == 4) {
    // HR only
    if (
      applicationDeadline.value == "" ||
      applicationOpening.value == "" ||
      selectedCountry.value == "" ||
      selectedDept.value == "" ||
      managerID.value == "" ||
      selectedTitle.value == ""
    ) {
      errorMessage.value = "Not all fields are filled!";
      isOpen.value = true;
    } else {
      const body = {
        application_deadline: applicationDeadline.value,
        application_opening: applicationOpening.value,
        country: selectedCountry.value,
        dept: selectedDept.value,
        manager_ID: managerID.value,
        role_name: selectedTitle.value,
      };
      axios
        .post(`${backend_url.value}/addrolelisting`, body)
        .then((response) => {
          isOpen.value = true;
          isSuccess.value = true;
          for (const key in response.data) {
              roleListingId.value = key;
          }
        })
        .catch((error) => {
          errorMessage.value = error.message;
          isOpen.value = true;
        });
    }
  } else {
    // not admin
    errorMessage.value = "Unauthorised access!";
    isOpen.value = true;
  }
}

function goBack() {
  this.$router.push(-1);
}

function updateSkills() {
  axios
    .get(`${backend_url.value}/get_role_skill/${selectedTitle.value}`)
    .then((response) => {
      skills.value = response.data.data;
    })
    .catch((error) => {
      console.log(error.message);
    });
}
</script>

<template>
  <div class="bg-beige min-h-screen px-10">
    <router-link
      id="backButton"
      to="/home"
      class="w-full flex w-1/2 px-5 py-2 text-sm text-gray-700 transition-colors duration-200 rounded-lg gap-x-2 sm:w-auto dark:hover:bg-gray-800 dark:bg-gray-900 hover:bg-gray-100 dark:text-gray-200 dark:border-gray-700"
    >
      <svg
        class="w-5 h-5 rtl:rotate-180"
        xmlns="http://www.w3.org/2000/svg"
        fill="none"
        viewBox="0 0 24 24"
        stroke-width="1.5"
        stroke="currentColor"
      >
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          d="M6.75 15.75L3 12m0 0l3.75-3.75M3 12h18"
        />
      </svg>
    </router-link>
    <p class="font-serif flex justify-center items-center">Add Role Listing</p>
    <div class="bg-grey-50 rounded-lg p-5 mt-5 font-sans text-base">
      <div class="grid grid-cols-3 gap-28">
        <div>
          <p class="font-bold">Title</p>
          <select
            class="mt-1 p-2 rounded-md w-full"
            v-model="selectedTitle"
            @change="updateSkills"
            id="title"
          >
            <option v-for="(description, role) in roles" :key="description">
              {{ role }}
            </option>
          </select>
        </div>
        <div>
          <label for="applicationOpening" class="block font-bold"
            >Application Opening</label
          >
          <input
            type="date"
            id="applicationOpening"
            name="applicationOpening"
            class="mt-1 p-2 rounded-md w-full"
            v-model="applicationOpening"
            :min="minOpenDate"
            @change="updateMinCloseDate"
            @input="validateApplicationOpening"
          />
        </div>
        <div>
          <label for="applicationDeadline" class="block font-bold"
            >Application Deadline</label
          >
          <input
            type="date"
            id="applicationDeadline"
            name="applicationDeadline"
            class="mt-1 p-2 rounded-md w-full"
            v-model="applicationDeadline"
            :min="minCloseDate"
            @input="validateApplicationDeadline"
          />
        </div>
      </div>
      <div class="grid grid-cols-3 pt-5 gap-28">
        <div>
          <p class="font-bold">Hiring Department</p>
          <select class="mt-1 p-2 rounded-md w-full" v-model="selectedDept" id="department">
            <option v-for="dept of hiringDepartment" :key="dept">
              {{ dept }}
            </option>
          </select>
        </div>
        <div>
          <p class="font-bold">Country</p>
          <select class="mt-1 p-2 rounded-md w-full" v-model="selectedCountry" id="country">
            <option v-for="country of countries" :key="country">
              {{ country }}
            </option>
          </select>
        </div>
        <div>
          <p class="font-bold">Reporting Manager</p>
          <select
            id="manager"
            class="mt-1 p-2 rounded-md w-full"
            v-model="managerID"
          >
            <option v-for="(name, id) in staff" :key="id" :value="id">
              {{ name }} ({{ id }})
            </option>
          </select>
        </div>
      </div>
      <div class="pt-5">
        <p class="font-bold">Description</p>
        <textarea
          :value="roles[selectedTitle]"
          disabled
          class="w-full h-24 p-2 bg-white rounded-md text-grey"
        >
        </textarea>
      </div>
      <div class="pt-5">
        <p class="font-bold">Required Skills</p>
        <label class="flex text-grey" v-for="skill of skills" :key="skill">
          <input type="checkbox" :value="skill" checked disabled />
          <p class="ml-2">{{ skill }}</p>
        </label>
      </div>
    </div>
    <Button @click="addRoleListing">
      <template v-slot:text>Add Role Listing</template>
    </Button>

    <div id="roleListingId" style="display: none;">
        {{ roleListingId }}
    </div>

    <Modal v-if="isOpen" :isSuccess="isSuccess">
      <template v-slot:text>
        <p v-if="isSuccess" id="successMessage">Role listing has been added successfully.</p>
        <p v-else id="errorMessage">{{ errorMessage }}</p>
      </template>
    </Modal>
  </div>
</template>
