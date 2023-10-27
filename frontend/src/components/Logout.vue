<script setup>
    import { ref } from "vue";
    import { useUserStore } from "@/store/useUserStore";
    import { storeToRefs } from 'pinia';
    import router from '@/router';

    const store = useUserStore();
    const {
        user,
    } = storeToRefs(store);

    const access = {1: 'Admin', 2: 'Staff', 3: 'Manager', 4: 'HR Staff'};

    const isExpand = ref(false);

    function expandDropdown() {
        isExpand.value = !isExpand.value;
    }

    function logout() {
        router.push({name: 'Login'});
        user.value = null;
    }
</script>

<template>
<div class="bg-white font-serif">
    <div class="grid grid-cols-3 py-3 items-center">
        <div>
            <img class="w-16" src="@/assets/logo.png" alt="">
        </div>
        <div class="mx-auto text-lg">
            <router-link id="viewRoute" :class="$route.name === 'Home' ? 'font-semibold text-yellow' : ''" to="/home">
                View
            </router-link>
            <router-link id="manageRoute" class="ml-12" v-if="user.access_ID == 4" :class="$route.name === 'Role Listing Management' ? 'font-semibold text-yellow' : ''" to="/rolelistingmanagement">
                Manage
            </router-link>
        </div>
        <div class="ml-auto">
            <div class="flex ml-auto items-center relative">
                <img v-if="user.access_ID == 4" src="@/assets/hr_staff.svg" alt="">
                <img v-else-if="user.access_ID == 3" src="@/assets/manager.svg" alt="">
                <img v-else src="@/assets/staff.svg" alt="">
                <div class="ml-2">
                    <p class="text-base">{{ user.staff_FName + " " + user.staff_LName }}</p>
                    <p class="text-xs">{{ access[user.access_ID] }}</p>
                </div>
                <img class="ml-3 cursor-pointer" src="@/assets/icons/dropdown.svg" alt="" @click="expandDropdown">
            </div>
        </div>
    </div>
    <div v-if="isExpand" class="absolute right-0 mr-10 bg-grey-50 text-sm cursor-pointer">
        <div class="flex w-36 p-3 rounded-md hover:bg-grey">
            <img class="mr-2" src="@/assets/icons/folder.svg" alt="">
            <p>My Skill Profile</p>
        </div>
        <div class="flex w-36 p-3 rounded-md hover:bg-grey" @click="logout">
            <img class="mr-2" src="@/assets/icons/logout.svg" alt="">
            <p>Logout</p>
        </div>
    </div>
</div>
</template>