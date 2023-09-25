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
  <div class="bg-beige min-h-screen px-10 py-5">
    <h1 class="text-center">Manage Role Listing</h1>
    <ul>
      <li class="flex border-t-2 ">
        <div class="flex-none h-100 ">
          <div> Software Engineer </div>
          <div> Reporting Manager: 1003 </div>
          <div class="flex flex-row"> 
            <div> Apply by 5 September 2023 </div>
            <div class="flex items-center mx-2">
              <span class="bg-black h-1 w-1 rounded-full"></span>
            </div>
            <div> 11 applicants </div>
          </div>
        </div>
        <div class="grow"></div>
        <div class="flex flex-row items-center">
          <div>Engineering Operation</div>
          <div class="flex bg-black mx-2 h-1 w-1 rounded-full"> </div>
          <div>Hong Kong</div>
        </div>
      </li>
      <li class="border-t-2">Database Admin</li>
      <li class="border-t-2">Financial Analyst</li>
    </ul>
  </div>
</template>

<style></style>