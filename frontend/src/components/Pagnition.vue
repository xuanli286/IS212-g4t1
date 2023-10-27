<template>
    <div class="flex justify-end">
        <div class="flex space-x-4 rounded-md bg-white w-fit p-2">
            <button class="btn-white min_button" @click="start" :disabled="modelValue == 1">
                <i class="bi bi-chevron-bar-left"></i>
            </button>
            <button class="btn-white back_button" @click="decrement" :disabled="modelValue <= 1">
                <i class="bi bi-chevron-left"></i>
            </button>
            <input class="input-search border-gray-500" min="1" :max="maxPage" :value="modelValue" @blur="registerValue" @keydown.enter="registerValue" ref="inputField">
            <p>of</p>
            <p class="max_page"> {{ maxPage }}</p>
            <button class="btn-white right_button" @click="increment" :disabled="modelValue >= maxPage">
                <i class="bi bi-chevron-right"></i>
            </button>
            <button class="btn-white max_button" @click="end" :disabled="modelValue == maxPage">
                <i class="bi bi-chevron-bar-right"></i>
            </button>
        </div>
    </div>
</template>

<script setup>
    import { defineProps, defineEmits, ref, computed } from 'vue';

    const props = defineProps(['modelValue', 'maxPage']);
    const emit = defineEmits(['update:modelValue']);

    const inputField = ref()

    const start = () => {
        emit('update:modelValue', 1);
    };

    const decrement = () => {
        if (props.modelValue > 1) {
            emit('update:modelValue', props.modelValue - 1);
        }
    };

    const increment = () => {
        if (props.modelValue < props.maxPage) {
            emit('update:modelValue', props.modelValue + 1);
        }
    };

    const end = () => {
        emit('update:modelValue', props.maxPage);
    };

    const registerValue = () => {
        const inputValue = Number(inputField.value.value);

        if (inputValue <= 0) {
            start();
        } else if (inputValue > props.maxPage) {
            end();
        } else if (isNaN(Number(inputValue)) || !(inputValue >= 1 && inputValue <= props.maxPage)) {
            start();
        } else {
            emit('update:modelValue', inputValue);
        }
    };
    
</script>
  
<style scoped>
    .input-search {
        @apply
        bg-white
        rounded-md
        w-16
        border
        text-center
        focus:outline-none
        
    }

</style>