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
    <h1 class="mx-64 text-center py-10 text-xl font-serif" id="roleListings">Manage Role Listing</h1>
    <ul class="mx-64">
      <li class="flex border-t-2 py-5 hover:bg-grey-50">
        <div class="flex-none h-100">
          <div class="text-yellow text-xl"> Software Engineer </div>
          <div class="text-base"> Reporting Manager: 1003 </div>
          <div class="flex flex-row text-xs"> 
            <div class="text-grey"> Apply by 5 September 2023 </div>
            <div class="flex items-center mx-2">
              <span class="bg-black h-1 w-1 rounded-full"></span>
            </div>
            <div class="font-bold text-green"> 11 applicants </div>
          </div>
        </div>
        <div class="grow"></div>
        <div>
          <div class="flex flex-row ">
            <div class="grow"></div>
            <div class="me-5 text-xs bg-red px-4 py-1 rounded-full text-white">Closed</div>
          </div>
          <div class="flex flex-row items-center text-yellow pt-3">
            <div class="font-bold">Engineering Operation</div>
            <div class="flex bg-yellow mx-2 h-1 w-1 rounded-full"> </div>
            <div>Hong Kong</div>
          </div>
        </div>
      </li>
      <li class="flex border-t-2 py-5 hover:bg-grey-50">
        <div class="flex-none h-100">
          <div class="text-yellow text-xl"> Software Engineer </div>
          <div class="text-base"> Reporting Manager: 1003 </div>
          <div class="flex flex-row text-xs"> 
            <div class="text-grey"> Apply by 5 September 2023 </div>
            <div class="flex items-center mx-2">
              <span class="bg-black h-1 w-1 rounded-full"></span>
            </div>
            <div class="font-bold text-green"> 11 applicants </div>
          </div>
        </div>
        <div class="grow"></div>
        <div>
          <div class="flex flex-row ">
            <div class="grow"></div>
            <div class="me-5 text-xs bg-green px-4 py-1 rounded-full text-white">Open</div>
          </div>
          <div class="flex flex-row items-center text-yellow pt-3">
            <div class="font-bold">Engineering Operation</div>
            <div class="flex bg-yellow mx-2 h-1 w-1 rounded-full"> </div>
            <div>Hong Kong</div>
          </div>
        </div>
      </li>
      <li class="flex border-t-2 py-5 hover:bg-grey-50">
        <div class="flex-none h-100">
          <div class="text-yellow text-xl"> Software Engineer </div>
          <div class="text-base"> Reporting Manager: 1003 </div>
          <div class="flex flex-row text-xs"> 
            <div class="text-grey"> Apply by 5 September 2023 </div>
            <div class="flex items-center mx-2">
              <span class="bg-black h-1 w-1 rounded-full"></span>
            </div>
            <div class="font-bold text-green"> 11 applicants </div>
          </div>
        </div>
        <div class="grow"></div>
        <div>
          <div class="flex flex-row ">
            <div class="grow"></div>
            <div class="me-5 text-xs bg-green px-4 py-1 rounded-full text-white">Open</div>
          </div>
          <div class="flex flex-row items-center text-yellow pt-3">
            <div class="font-bold">Engineering Operation</div>
            <div class="flex bg-yellow mx-2 h-1 w-1 rounded-full"> </div>
            <div>Hong Kong</div>
          </div>
        </div>
      </li>
    </ul>
  </div>
</template>

<style></style>