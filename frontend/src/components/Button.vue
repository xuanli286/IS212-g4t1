<script setup>

</script>

<template>
    <div class="mt-5 flex justify-end">
        <button class="bg-yellow hover:bg-yellow-50 rounded-2xl text-white font-sans text-sm w-auto px-5 py-2 flex">
            <slot name="icon"></slot>
            <slot name="text"></slot>
        </button>
    </div>
</template>