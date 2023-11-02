<template>
    <div>
        <h2 class="text-xl font-serif text-center pt-24 mb-5">Find a Promising Candidate with us!</h2>
        <div class="mb-14">

        </div>
        <div class="grid grid-cols-4 gap-2">
            <div class="flex justify-between items-center col-end-5 col-span-3 mx-2">
                <div class="text-sm records">
                    Showing {{ (page - 1) * 20 + 1 }} - {{ Math.min(page * 20, filteredStaffs.length) }} of
                    {{ filteredStaffs.length }} staff
                </div>
                <Pagnition :maxPage="Math.max(1, Math.ceil(filteredStaffs.length / 20))" v-model="page" />
            </div>
            <div>
                <FilterComponent class="w-full ml-2" :countries="countries" :hiringDepartments="hiringDepartment"
                    :roleListings="rolelistings" :inCandidates="inCandidates" :userSkills="allSkills"
                    @filter-updated="updateFilter" @filter-cleared="clearFilter" />
            </div>
            <div v-if="filteredStaffs.length > 0" class="col-span-3 grid grid-cols-4 gap-3 mx-2 self-start">
                <div class="white-card cursor-pointer" v-for="staffInfo of filteredStaffs.slice((page - 1) * 20, page * 20)"
                    @click="goToStaff(staffInfo.staff_ID)">
                    <div v-show="allSkillsLength > 0" class="flex justify-end text-sm percentageMatch">
                        <div v-if="staffInfo.staff_skills.length > 0" class="bg-green rounded-lg text-white p-2">
                            {{ ((staffInfo.staff_skills.length / allSkillsLength) * 100).toFixed(2) }}%
                        </div>
                        <div v-else class="bg-white p-2 text-white">
                            0
                        </div>
                    </div>
                    <div class="flex justify-center">
                        <img :src="require(`@/assets/${getRandomInt()}.svg`)">
                    </div>
                    <h4 class="mt-2 text-yellow text-lg font-semibold staff_name">{{ staffInfo.staff_FName }} {{
                        staffInfo.staff_LName }}</h4>
                    <p class="text-sm mt-2 staff_ID"><i class="bi bi-person-badge"></i> {{ staffInfo.staff_ID }}</p>
                    <p class="text-xs mt-2 staff_email"><i class="bi bi-envelope-at-fill mr-2"></i><span
                            class="text-grey">{{
                                staffInfo.email }}</span></p>
                    <div class="flex justify-center content-center text-center text-yellow mt-2">
                        <div class="font-bold staff_dept">{{ staffInfo.dept }}</div>
                        <div class="bg-yellow mx-2 h-1 w-1 rounded-full place-self-center"> </div>
                        <div class="staff_country">{{ staffInfo.country }}</div>
                    </div>
                </div>
            </div>
            <div v-else class="col-span-3 mx-2 text-lg noMatch">
                <div class="text-center bg-red-50 font-semibold py-2 rounded-lg">
                    No matching Candidates!
                </div>
            </div>
            <div class="flex justify-between items-center col-end-5 col-span-3 mx-2">
                <div class="text-sm records">
                    Showing {{ (page - 1) * 20 + 1 }} - {{ Math.min(page * 20, filteredStaffs.length) }} of
                    {{ filteredStaffs.length }} staff
                </div>
                <Pagnition :maxPage="Math.max(1, Math.ceil(filteredStaffs.length / 20))" v-model="page" />
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
import Pagnition from '@/components/Pagnition.vue';
import FilterComponent from '@/components/FilterComponent.vue';
import router from "@/router";


const constStore = useConstantStore();
const { backend_url, countries, hiringDepartment } = storeToRefs(constStore);

const userStore = useUserStore();
const { user } = storeToRefs(userStore);


const staffs = ref([]);
const page = ref(1);
const selectedCountry = ref("all");
const selectedDept = ref("all");
const rolelistings = ref([]);
const inCandidates = ref(false);
const selectedSkills = ref([]);
const selectedRoleListing = ref("");
const allSkillsLength = ref(0);
const loaded = ref(false)
const allSkills = ref([])

axios.get(`${backend_url.value}/staff`)
    .then((response) => {
        let data = response.data.data.staff;

        staffs.value = []

        for (const item of data) {
            for (let key in item) {
                // console.log("outside" + key)
                item[key].staff_ID = key;
                staffs.value.push(item[key])
            }
        }
        console.log(staffs.value)

    })
    .catch((error) => {
        console.error(error)
    });

axios.get(`${backend_url.value}/get_all_skill`)
    .then(response => {
        let data = response.data.data

        for (const info of data) {
            allSkills.value.push(Object.keys(info)[0])
        }

    })
    .catch(error => {
        console.error(error)
    })

axios.get(`${backend_url.value}/openrolelisting?manager_ID=${user.value.staff_ID}`)
    .then((response) => {
        let data = response.data.data.rolelisting;

        for (let i = 0; i < data.length; i++) {

            let role_name = Object.values(data[i])[0].role_name

            if (!rolelistings.value.includes(role_name)) {
                rolelistings.value.push(role_name)
            }
        }

        console.log(rolelistings.value)
        inCandidates.value = true;

    })
    .catch((error) => {
        console.error(error)

    })

function getRandomInt() {
    return Math.floor(Math.random() * (10 - 1 + 1) + 1);
}

function goToStaff(staffId) {
    router.push(`/candidates/${staffId}`);
}

function updateFilter(data) {
    selectedCountry.value = data.selectedCountry;
    selectedDept.value = data.selectedDept;
    selectedRoleListing.value = data.selectedRoleListing;
    selectedSkills.value = data.selectedSkills;

    if (data.selectedRoleListing.length > 0) {
        axios.get(`${backend_url.value}/get_role_skill/${data.selectedRoleListing}`)
            .then((response) => {
                allSkillsLength.value = response.data.data.length;
            })
            .catch((error) => {
                console.error(error);
            });
    }

}

function clearFilter() {
    selectedCountry.value = "all";
    selectedDept.value = "all";
    selectedRoleListing.value = "";
    selectedSkills.value = [];
    allSkillsLength.value = 0;
}

const filteredStaffs = computed(() => {
    return staffs.value.filter((item) => {
        const countryFilter = selectedCountry.value === "all" || item.country === selectedCountry.value;
        const deptFilter = selectedDept.value === "all" || item.dept === selectedDept.value;
        const skillsFilter = selectedSkills.value.length === 0 || item.staff_skills.some((skill) => selectedSkills.value.includes(skill));

        return countryFilter && deptFilter && skillsFilter;
    });
});


</script>

<style scoped>
.white-card {
    @apply bg-white text-center rounded-lg px-2 py-6
}
</style>