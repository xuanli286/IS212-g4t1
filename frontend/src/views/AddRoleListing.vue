<template>
  <div class="bg-beige min-screen px-10 py-5">
        <p class="font-serif flex justify-center items-center">Add Role Listing</p>
        <div class="bg-grey-50 rounded-lg p-5 mt-5 font-sans text-base">
            <div class="grid grid-cols-3 gap-28">
                <div>
                    <p class="font-bold">Title</p>
                    <select class="mt-1 p-2 rounded-md w-full" v-model="selectedTitle" @change="updateSkills">
                        <option v-for="(description, role) in roles" :key="description">{{ role }}</option>
                    </select>
                </div>
                <div>
                    <label for="applicationOpening" class="block font-bold">Application Opening</label>
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
                    <label for="applicationDeadline" class="block font-bold">Application Deadline</label>
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
            <div class="grid grid-cols-2 pt-5 gap-16">
                <div>
                    <p class="font-bold">Hiring Department</p>
                    <select class="mt-1 p-2 rounded-md w-full" v-model="selectedDept">
                        <option v-for="dept of hiringDepartment" :key="dept">{{ dept }}</option>
                    </select>
                </div>
                <div>
                    <p class="font-bold">Country</p>
                    <select class="mt-1 p-2 rounded-md w-full" v-model="selectedCountry">
                        <option v-for="country of countries" :key="country">{{ country }}</option>
                    </select>
                    
                </div>
            </div>
            <div class="pt-5">
                <p class="font-bold">Description</p>
                <textarea
                    :value="roles[selectedTitle]"
                    disabled
                    class="w-full h-24 p-2 bg-white rounded-md text-grey"
                >
                </textarea>
            </div>
            <div class="pt-5">
                <p class="font-bold">Required Skills</p>
                <label class="flex text-grey" v-for="skill of skills" :key="skill">
                    <input type="checkbox" :value="skill" checked disabled />
                    <p class="ml-2">{{ skill }}</p>
                </label>
            </div>
        </div>
        <Button @click="addRoleListing">
            <template v-slot:text>Save Edit</template>
        </Button>

        <Modal v-if="isOpen" :isSuccess=isSuccess>
            <template v-slot:text>
                <p v-if="isSuccess">Role listing has been updated successfully.</p>
                <p v-else>{{ errorMessage }}</p>
            </template>
        </Modal>
    </div>
</template>

<script>
export default {
  name: 'AddRoleListing',
  components: {},
  props: {
  },
  data() {
    return {
    };
  },
  methods: {
  },
  created() {
  },
}
</script>

<style></style>