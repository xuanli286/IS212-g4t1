<script setup>
    import axios from "axios";
    import { ref, computed } from "vue";

    const rolelistingID = 1;
    
    const roles = ref({});
    const selectedTitle = ref("");
    const applicationOpening = ref("");
    const applicationDeadline = ref("");
    const minCloseDate = ref("");

    const today = new Date();

    const minOpenDate = computed(() => {
        let year = today.getFullYear();
        let month = String(today.getMonth() + 1).padStart(2, '0'); // Months are 0-indexed
        let day = String(today.getDate()).padStart(2, '0');
        return `${year}-${month}-${day}`;
    })

    applicationOpening.value = minOpenDate.value;

    function updateMinCloseDate() {
        const maxDate = new Date(Math.max(today, new Date(applicationOpening.value)));
        let year = maxDate.getFullYear();
        let month = String(maxDate.getMonth() + 1).padStart(2, '0'); // Months are 0-indexed
        let day = String(maxDate.getDate()).padStart(2, '0');
        minCloseDate.value = `${year}-${month}-${day}`
        console.log(maxDate)
    }

    axios.get(`http://127.0.0.1:5000/rolelisting/${rolelistingID}`)
        .then((response) => {
            const editRole = response.data.data[rolelistingID];
            selectedTitle.value = editRole.role_name;
            applicationOpening.value = editRole['application_opening'];
            applicationDeadline.value = editRole['application_deadline'];
            console.log(editRole)
        })
        .catch((error) => {
            console.log(error.message);
        })

    axios.get('http://127.0.0.1:5000/get_all_role')
        .then((response) => {
            for (let i of response.data.data) {
                for (let key in i) {
                    roles.value[key] = i[key];
                }
            }
        })
        .catch((error) => {
            console.log(error.message);
        })

    
</script>

<template>
    <div class="bg-white px-10 py-5">
        <p class="font-serif flex justify-center items-center">Edit Role Listing</p>
        <div class="bg-grey-50 rounded-lg p-5 mt-5">
            <div class="grid grid-cols-3 gap-28">
                <div>
                    <p class="font-sans font-bold text-base">Title</p>
                    <select class="mt-1 p-2 rounded-md w-full" v-model="selectedTitle">
                        <option v-for="(description, role) in roles" :key="description">{{ role }}</option>
                    </select>
                </div>
                <div>
                    <label for="applicationOpening" class="block font-sans font-bold text-base">Application Opening</label>
                    <input
                        type="date"
                        id="applicationOpening"
                        name="applicationOpening"
                        class="mt-1 p-2 rounded-md w-full"
                        v-model="applicationOpening"
                        :min="minOpenDate"
                        @change="updateMinCloseDate"
                    />
                </div>
                <div>
                    <label for="applicationDeadline" class="block font-sans font-bold text-base">Application Deadline</label>
                    <input
                        type="date"
                        id="applicationDeadline"
                        name="applicationDeadline"
                        class="mt-1 p-2 rounded-md w-full"
                        v-model="applicationDeadline"
                        :min="minCloseDate"
                    />
                </div>

            </div>
        </div>

        <!-- {{ roles[selectedTitle] }} -->
    </div>
</template>