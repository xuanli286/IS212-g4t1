<template>
   <!-- search bar -->
   <div>
      <form class="flex items-center pb-10" @submit.prevent="updateRoles">
        <label for="role-search" class="sr-only">Search</label>
        <div class="relative w-full">
          <div
            class="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none"
          >
          <img class="w-4 h-4" src="../assets/icons/bag.png" alt="">
          </div>
          <input
            type="text"
            v-model="search"
            @change="updateRoles()"
            id="role-search"
            class="bg-gray-50 border border-yellow text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full pl-10 p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 text-black dark:focus:ring-blue-500 dark:focus:border-blue-500"
            placeholder="Search Roles"
            required
          />
        </div>
        <button
          type="submit"
          @submit="updateRoles()"
          class="p-2.5 ml-2 text-sm font-medium text-blue bg-yellow rounded-lg border border-blue-700 hover:bg-yellow focus:ring-4 focus:outline-none focus:ring-yellow-300 dark:bg-yellow-600 dark:hover:bg-yellow-700 dark:focus:ring-yellow-800"
        >
          <svg
            class="w-4 h-4"
            aria-hidden="true"
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 20 20"
          >
            <path
              stroke="currentColor"
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="m19 19-4-4m0-7A7 7 0 1 1 1 8a7 7 0 0 1 14 0Z"
            />
          </svg>
          <span class="sr-only">Search</span>
        </button>
      </form>
    </div>
</template>

<script>

export default {
  data() {
    return {
        search: "",
    };
  },
  props: {
    searchQuery: String
  },
  methods: {
    async updateRoles(){
        console.log(this.search)
        this.$emit('search-updated', this.search);
    },
  },
};
</script>