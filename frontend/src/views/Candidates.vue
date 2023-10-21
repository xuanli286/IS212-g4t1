<template>

    <h2 class="text-xl font-serif text-center pt-24 mb-5">Find a Promising Candidate with us!</h2>
    <div class="mb-14">

    </div>
    <div class="grid grid-cols-4 gap-2">
        <div>
            <!-- for filter -->
        </div>
        <div class="col-span-3 grid grid-cols-4 gap-3 mx-2">
            <div class="flex justify-between items-center col-span-4">
                <div class="text-sm records">
                    Showing {{ (page-1) * 20 + 1 }} - {{ Math.min(page * 20, filteredStaffs.length) }} of {{filteredStaffs.length}} staff
                </div>
                <Pagnition :maxPage="Math.max(1, Math.ceil(filteredStaffs.length/20))" v-model="page"/>
            </div>
            <div class="white-card" v-for="staffInfo of filteredStaffs.slice( (page-1)*20, page*20 )">
                <div class="flex justify-center">
                    <img :src="require(`@/assets/${getRandomInt()}.svg`)">
                </div>
                <h4 class="mt-2 text-yellow text-lg font-semibold">{{ staffInfo.staff_FName }} {{ staffInfo.staff_LName }}</h4>
                <p class="text-sm mt-2"><i class="bi bi-person-badge"></i> {{ staffInfo.staff_ID }}</p>
                <p class="text-xs mt-2"><i class="bi bi-envelope-at-fill mr-2"></i><span class="text-grey">{{ staffInfo.email }}</span></p>
                <div class="flex justify-center content-center text-center text-yellow mt-2">
                    <div class="font-bold">{{ staffInfo.dept }}</div>
                    <div class="role-department bg-yellow mx-2 h-1 w-1 rounded-full place-self-center"> </div>
                    <div class="role-country">{{ staffInfo.country }}</div>
                </div>
            </div>
            <div class="flex justify-between items-center col-span-4 mb-5">
                <div class="text-sm records">
                    Showing {{ (page-1) * 20 + 1 }} - {{ Math.min(page * 20, filteredStaffs.length) }} of {{filteredStaffs.length}} staff
                </div>
                <Pagnition :maxPage="Math.max(1, Math.ceil(filteredStaffs.length/20))" v-model="page"/>
            </div>
        </div>
    </div>
    
</template>


<script setup>
import axios from "axios";
import { ref, computed } from "vue";
import { storeToRefs } from 'pinia';
import { useUserStore } from "@/store/useUserStore";
import { useConstantStore } from '@/store/useConstantStore';
import { useRoute } from 'vue-router';
import Pagnition from '@/components/Pagnition.vue'


const constStore = useConstantStore();
const { backend_url } = storeToRefs(constStore);

const userStore = useUserStore();


const staffs = ref([]);
const page = ref(1);


axios.get(`${backend_url.value}/staff`)
     .then((response) => {
        let data = response.data.data.staff;

        staffs.value = []

        for (const item of data) {
            for (const key in item) {
                item[key].staff_ID = key
                staffs.value.push(item[key]);
            }
        }

        // console.log(staffs.value)
     })
     .catch((error) => {
        console.error(error)
     });

function getRandomInt() {
    return Math.floor(Math.random() * (10 - 1 + 1) + 1);
}

const filteredStaffs = computed(() => {
    if (false) {
        // for filter
    }
    return staffs.value;
});

</script>

<style scoped>
    .white-card {
        @apply
        bg-white
        text-center
        rounded-lg
        px-2
        py-6
    }
</style>