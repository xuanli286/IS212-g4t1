<script setup>
    import { ref } from "vue";
    const user = {access_ID: 2, staff_FName: "Philip", staff_LName: "Lee"};
    const access = {0: 'Staff', 1: 'Manager & Director', 2: 'HR Staff'};

    const isExpand = ref(false);

    function expandDropdown() {
        isExpand.value = !isExpand.value;
    }
</script>

<template>
    <div class="font-serif">
        <div class="flex">
            <img class="w-16" src="@/assets/logo.png" alt="">
            <div class="flex ml-auto items-center relative">
                <img src="@/assets/hr_staff.svg" alt="">
                <div class="ml-2">
                    <p class="text-base">{{ user.staff_FName + " " + user.staff_LName }}</p>
                    <p class="text-xs">{{ access[user.access_ID] }}</p>
                </div>
                <img class="ml-3 cursor-pointer" src="@/assets/icons/dropdown.svg" alt="" @click="expandDropdown">
            </div>
        </div>
        <div v-if="isExpand" class="absolute right-0 mr-10 bg-grey-50 text-xs cursor-pointer">
            <div class="flex w-36 p-3 rounded-md hover:bg-grey">
                <img class="mr-2" src="@/assets/icons/folder.svg" alt="">
                <p>My Skill Profile</p>
            </div>
            <div class="flex w-36 p-3 rounded-md hover:bg-grey">
                <img class="mr-2" src="@/assets/icons/logout.svg" alt="">
                <p>Logout</p>
            </div>
        </div>
    </div>
</template>