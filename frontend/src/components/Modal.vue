<script setup>
    import { useEditRoleListingStore } from "@/store/useEditRoleListingStore.js";
    import { storeToRefs } from 'pinia';

    const store = useEditRoleListingStore();
    const {
        isOpen,
        isSuccess,
    } = storeToRefs(store);

    function closeModal() {
        isOpen.value = false;
        isSuccess.value = false;
    }
</script>

<template>
    <div>
        <div id="modal" class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-70 font-sans text-black">
            <div 
                class="shadow-lg rounded-lg px-6 py-4 w-1/2 relative flex"
                :class="isSuccess ? 'bg-green-50' : 'bg-red-50'"
            >
                <p class="absolute right-5 cursor-pointer" @click="closeModal">X</p>
                <div class="flex">
                    <img class="w-8 mr-3" v-if="isSuccess" src="@/assets/icons/success.svg" alt="">
                    <img class="w-8 mr-3" v-else src="@/assets/icons/error.svg" alt="">
                    <div class="items-center">
                        <p v-if="isSuccess" class="text-green font-bold">Success</p>
                        <p v-else class="text-red font-bold">Error</p>
                        <slot name="text"></slot>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>