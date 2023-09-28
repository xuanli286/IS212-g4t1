<script setup>
import axios from "axios";
import Button from "@/components/Button.vue";
import Modal from "@/components/Modal.vue";
import { ref, computed } from "vue";
import { storeToRefs } from 'pinia';
import { useConstantStore } from '@/store/useConstantStore';
import { useModalStore } from "@/store/useModalStore";
import { useRoute } from 'vue-router';

const store = useModalStore();
const {
    isOpen,
    isSuccess,
} = storeToRefs(store);

const constStore = useConstantStore();
const {
    hiringDepartment,
    countries,
} = storeToRefs(constStore);

const route = useRoute();
const rolelistingID = route.params.id;

const roles = ref({});
const selectedTitle = ref("");
const applicationOpening = ref("");
const applicationDeadline = ref("");
const selectedDept = ref("");
const selectedCountry = ref("");
const skills = ref([]);
const managerID = ref([]);
const errorMessage = ref("");

const today = new Date();

const minOpenDate = computed(() => {
    let year = today.getFullYear();
    let month = String(today.getMonth() + 1).padStart(2, '0');
    let day = String(today.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
})

applicationOpening.value = minOpenDate.value;

const minCloseDate = computed(() => {
    const dates = [new Date(applicationOpening.value), today];
    const maxDate = new Date(Math.max.apply(null, dates));
    maxDate.setDate(maxDate.getDate() + 1);
    const year = maxDate.getFullYear();
    const month = String(maxDate.getMonth() + 1).padStart(2, '0');
    const day = String(maxDate.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
});

function updateMinCloseDate() {
    const dates = [new Date(applicationOpening.value), today];
    const maxDate = new Date(Math.max.apply(null, dates));
    maxDate.setDate(maxDate.getDate() + 1);
    let year = maxDate.getFullYear();
    let month = String(maxDate.getMonth() + 1).padStart(2, '0');
    let day = String(maxDate.getDate()).padStart(2, '0');
    minCloseDate.value = `${year}-${month}-${day}`;
    applicationDeadline.value = minCloseDate.value;
}

axios.get(`http://127.0.0.1:5000/rolelisting/${rolelistingID}`)
    .then((response) => {
        const editRole = response.data.data[rolelistingID];
        selectedTitle.value = editRole.role_name;
        updateSkills();
        applicationOpening.value = editRole['application_opening'];
        applicationDeadline.value = editRole['application_deadline'];
        selectedDept.value = editRole.dept;
        selectedCountry.value = editRole.country;
        managerID.value = editRole['manager_ID'];
        console.log(editRole);
    })
    .catch((error) => {
        console.log(error.message);
    })

axios.get('http://127.0.0.1:5000/get_all_role')
    .then((response) => {
        for (let i of response.data.data) {
            for (let key in i) {
                roles.value[key] = i[key];
            }
        }
    })
    .catch((error) => {
        console.log(error.message);
    })

function updateSkills() {
    axios.get(`http://127.0.0.1:5000/get_role_skill/${selectedTitle.value}`)
        .then((response) => {
            skills.value = response.data.data;
        })
        .catch((error) => {
            console.log(error.message);
        })
}

function editRoleListing() {
    const body = {
        "application_deadline": applicationDeadline.value,
        "application_opening": applicationOpening.value,
        "country": selectedCountry.value,
        "dept": selectedDept.value,
        "manager_ID": managerID.value,
        "role_name": selectedTitle.value,
    }
    axios.put(`http://127.0.0.1:5000/updaterolelisting/${rolelistingID}`, body)
        .then((response) => {
            isOpen.value = true;
            isSuccess.value = true;
        })
        .catch((error) => {
            errorMessage.value = error.response.data.message;
            isOpen.value = true;
        })
}
</script>

<template>
<div class="bg-beige px-10 py-5">
    <p class="font-serif flex justify-center items-center">Edit Role Listing</p>
    <div class="bg-grey-50 rounded-lg p-5 mt-5 font-sans text-base">
        <div class="grid grid-cols-3 gap-28">
            <div>
                <p class="font-bold">Title</p>
                <select class="mt-1 p-2 rounded-md w-full" v-model="selectedTitle" @change="updateSkills">
                    <option v-for="(description, role) in roles" :key="description">{{ role }}</option>
                </select>
            </div>
            <div>
                <label for="applicationOpening" class="block font-bold">Application Opening</label>
                <input
                    type="date"
                    id="applicationOpening"
                    name="applicationOpening"
                    class="mt-1 p-2 rounded-md w-full"
                    v-model="applicationOpening"
                    :min="minOpenDate"
                    @change="updateMinCloseDate"
                />
            </div>
            <div>
                <label for="applicationDeadline" class="block font-bold">Application Deadline</label>
                <input
                    type="date"
                    id="applicationDeadline"
                    name="applicationDeadline"
                    class="mt-1 p-2 rounded-md w-full"
                    v-model="applicationDeadline"
                    :min="minCloseDate"
                />
            </div>
        </div>
        <div class="grid grid-cols-2 pt-5 gap-16">
            <div>
                <p class="font-bold">Hiring Department</p>
                <select class="mt-1 p-2 rounded-md w-full" v-model="selectedDept">
                    <option v-for="dept of hiringDepartment" :key="dept">{{ dept }}</option>
                </select>
            </div>
            <div>
                <p class="font-bold">Country</p>
                <select class="mt-1 p-2 rounded-md w-full" v-model="selectedCountry">
                    <option v-for="country of countries" :key="country">{{ country }}</option>
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
    <Button @click="editRoleListing">
        <template v-slot:icon>
            <img class="mr-2" src="@/assets/icons/edit.svg" alt="">
        </template>
        <template v-slot:text>Save Edit</template>
    </Button>

    <Modal v-if="isOpen" :isSuccess=isSuccess>
        <template v-slot:text>
            <p v-if="isSuccess">Role listing has been updated successfully.</p>
            <p v-else>{{ errorMessage }}</p>
        </template>
    </Modal>
</div>
</template>