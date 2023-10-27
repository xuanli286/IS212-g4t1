<script setup>
    import { ref, onMounted } from "vue";
    import { useUserStore } from "@/store/useUserStore";
    import { useConstantStore } from "@/store/useConstantStore";
    import { storeToRefs } from 'pinia';

    const userStore = useUserStore();
    const {
        user,
    } = storeToRefs(userStore);

    const store = useConstantStore();
    const {
        staffSkills,
    } = storeToRefs(store);

    const access = {1: 'Admin', 2: 'Staff', 3: 'Manager', 4: 'HR Staff'};

    onMounted(async () => {
        try {
            store.getStaffSkills(user.value.staff_ID);
        }
        catch (error) {
            console.log(error.message);
        }
    })

</script>

<template>
    <div class="bg-white p-10 mt-1 mx-5 text-center rounded-lg">
        <img class="w-48 mx-auto" v-if="user.access_ID == 4" src="@/assets/hr_staff.svg" alt="">
        <img class="w-48 mx-auto" v-else-if="user.access_ID == 3" src="@/assets/manager.svg" alt="">
        <img class="w-48 mx-auto" v-else src="@/assets/staff.svg" alt="">
        <div class="flex items-center justify-center font-serif">
            <p class="mt-3 text-lg font-semibold text-yellow">{{ user.staff_FName }} {{ user.staff_LName }}</p>
            <p class="p-1 w-16 rounded-2xl bg-yellow text-white text-xs ml-2 mt-3">
                {{ user.staff_ID }}
            </p>
        </div>
        <div class="grid gap-x-0 gap-y-2 grid-cols-2 text-start mt-4">
            <div>
                <p class="font-bold">Country</p>
            </div>
            <div id="country">
                <p>{{ user.staff_country }}</p>
            </div>
            <div>
                <p class="font-bold">Department</p>
            </div>
            <div id="dept">
                <p>{{ user.staff_dept }}</p>
            </div>
            <div>
                <p class="font-bold">Email</p>
            </div>
            <div id="email">
                <p>{{ user.staff_email }}</p>
            </div>
            <div>
                <p class="font-bold">Skills</p>
            </div>
            <div id="skill" v-if="staffSkills.length == 0">
                No available skill
            </div>
            <div id="skill" v-else>
                <ul class="list-disc ml-5" v-for="skill of staffSkills" :key="skill">
                    <li>{{ skill }}</li>
                </ul>
            </div>
        </div>
    </div>
</template>