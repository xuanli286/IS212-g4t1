<script setup>
  import axios from "axios";

  var roleListings = []
  axios
    .get("http://127.0.0.1:5000/openrolelisting")
    .then((response) => {
      roleListings = cleanResponseData(response)
      console.log(roleListings);

    })

  function cleanResponseData(response){
    roleListings = response.data.data.rolelisting
    var cleanedRoleListings = []
      for(let i = 0; i < roleListings.length; i++){
        let key = Object.keys(roleListings[i])
        let roleListingObj = roleListings[i][key]
        cleanedRoleListings.push(roleListingObj)
      }
    return cleanedRoleListings
  }

</script>

<template>
  <div>
    <h1>Role Listing Management</h1>
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