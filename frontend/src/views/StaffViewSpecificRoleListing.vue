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
                        <span class="font-light ml-1">{{ new Date(roleDetails.application_deadline).toLocaleDateString('en-US', { day: 'numeric', month: 'long', year: 'numeric' }) }}</span>
                    </p>
                </div>
            </div>
            <Button id="apply" class="ml-auto" @click="applyRole">
                <template v-slot:icon>
                    <img class="mr-1" src="@/assets/icons/attachdocument.svg" alt="">
                </template>
                <template v-slot:text>
                    Apply Role
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
        <div class="mt-10 rounded-lg bg-white p-5">
            <div class="flex items-center">
                <img src="@/assets/icons/puzzle.svg" alt="">
                <p class="font-bold text-yellow ml-1">Skills Match</p>
            </div>
            <div class="ml-8">
                <p class="mt-2 font-serif text-green text-sm" id="percentage">{{ (matchedSkills.length/roleSkills.length*100).toFixed(0) }}% skills match</p>
                <div class="flex gap-1">
                    <img v-for="skill of matchedSkills.length" :key="skill" src="@/assets/matchedSkill.svg" alt="">
                    <img v-for="skill of missingSkills.length" :key="skill" src="@/assets/unmatchedSkill.svg" alt="">
                </div>
                <div class="mt-2">
                    <div class="flex items-center">
                        <img src="@/assets/icons/check.svg" alt="">
                        <p class="font-bold text-sm ml-1">{{ matchedSkills.length }} skills on your profile</p>
                    </div>
                    <p class="ml-4 text-sm" id="matched-skills">
                        <span v-if="matchedSkills.length > 0">{{ matchedSkills.join(', ') }}</span>
                        <span v-else class="text-grey">No matching skill found</span>
                    </p>
                </div>
                <div class="mt-2">
                    <div class="flex items-center">
                        <img src="@/assets/icons/exclamation.svg" alt="">
                        <p class="font-bold text-sm ml-1">{{ missingSkills.length }} skills missing on your profile</p>
                    </div>
                    <p class="ml-4 text-sm" id="missing-skills">
                        <span v-if="missingSkills.length > 0">{{ missingSkills.join(', ') }}</span>
                        <span v-else class="text-grey">All skills matched</span>
                    </p>
                </div>
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
        staffSkills,
        backend_url,
    } = storeToRefs(store);

    const rolelistingID = route.params.id;
    const roleName = ref("");
    const roleDetails = ref({});

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

    const matchedSkills = computed(() => {
        const matched = [];
        for (let skill of roleSkills.value) {
            if (staffSkills.value.indexOf(skill) !== -1) {
                matched.push(skill);
            }
        }
        return matched;
    });

    const missingSkills = computed(() => {
        const missing = [];
        for (let skill of roleSkills.value) {
            if (staffSkills.value.indexOf(skill) === -1) {
                missing.push(skill);
            }
        }
        return missing;
    });

    function back() {
        window.history.back();
    }

    function applyRole() {
        // TO-DO:
        router.push({name: 'applyRole'});
    }
</script>