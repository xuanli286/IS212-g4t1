<script setup>
    import { ref } from "vue";
    import { useUserStore } from "@/store/useUserStore";
    import { storeToRefs } from 'pinia';
    import router from '@/router';

    const store = useUserStore();
    const {
        user,
    } = storeToRefs(store);

    const access = {0: 'Staff', 1: 'Manager & Director', 2: 'HR Staff'};

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
    <div class="flex py-3 items-center">
        <img class="w-16" src="@/assets/logo.png" alt="">
        <div class="ml-auto">
            <router-link v-if="user.access_ID > 0" :class="$route.name === 'Home' ? 'font-semibold text-yellow' : ''" to="/home">
                Manage
            </router-link>
            <router-link class="ml-12" :class="$route.name === 'ViewRoleListing' || (user.access_ID == 0 && $route.name === 'Home') ? 'font-semibold text-yellow' : ''" to="/viewrolelisting">
                View
            </router-link>
        </div>
        <div class="flex ml-auto items-center relative">
            <img v-if="user.access_ID == 0" src="@/assets/staff.svg" alt="">
            <img v-else-if="user.access_ID == 2" src="@/assets/hr_staff.svg" alt="">
            <img v-else src="@/assets/manager.svg" alt="">
            <div class="ml-2">
                <p class="text-base">{{ user.staff_FName + " " + user.staff_LName }}</p>
                <p class="text-xs">{{ access[user.access_ID] }}</p>
            </div>
            <img class="ml-3 cursor-pointer" src="@/assets/icons/dropdown.svg" alt="" @click="expandDropdown">
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