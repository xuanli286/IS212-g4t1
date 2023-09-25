<script setup>
  import axios from "axios";
  import { ref } from "vue";

  const roleListings = ref({})

  axios
    .get("http://127.0.0.1:5000/openrolelisting")
    .then((response) => {
      let receivedListings = response.data.data.rolelisting
      for(let listing of receivedListings){
        for(let key in listing){
          roleListings.value[key] = listing[key]
        }
      }
      console.log(roleListings);
    });

</script>

<template>
  <div>
    <h1>Role Listing Management</h1>
    <ul>
    </ul>
  </div>
</template>

<!-- <script>
export default {
  name: 'RoleListingManagement',
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
</script> -->

<style></style>