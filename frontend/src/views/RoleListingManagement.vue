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
    });

  axios
    .get("http://127.0.0.1:5000/closerolelisting")
    .then((response) => {
      let receivedListings = response.data.data.rolelisting
      for(let listing of receivedListings){
        for(let key in listing){
          roleListings.value[key] = listing[key]
        }
      }
    });

  function checkOpen(listing){
    let today = new Date();
    let deadline = new Date(listing.application_deadline)
    if(deadline > today){
        return true
      }
    
    return false
  }  

  function formatDate(dateString){
    let date = new Date(dateString)
    let day = date.getDate() 
    let month = date.toLocaleString('default', { month: 'long' });
    let year = date.getFullYear()
    return `${day} ${month} ${year}`
  }
</script>

<template>
  <div class="bg-beige min-h-screen px-10 py-5">
    <div class="flex flex-row mx-64">
      <div class="flex flex-row grow py-20 text-xl font-serif text-center " id="roleListings">
        <div class="grow"></div>
        <h1 class="translate-x-[85px]">Manage Role Listing</h1>
        <div class="grow"></div>
      </div>
      <div class="flex items-center">
        <router-link id="addRoleListingButton" to="/addrolelisting" class="flex flex-row bg-yellow py-2 px-5 rounded-full text-white text-sm" >
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6 me-2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v6m3-3H9m12 0a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <div class="my-auto">Add Role Listing</div>
        </router-link>
      </div>
    </div>
    <ul class="mx-64 min-w-fit rolelisting-container">
      <li v-for="(listing, id) in roleListings" :key="id" class="rolelisting-panel flex border-t py-5 hover:bg-grey-50">
        <div class="flex-none h-100">
          <div label="role-title" class="text-yellow text-xl"> {{listing.role_name}} </div>
          <div label="role-manager" class="text-base"> Reporting Manager: {{listing.manager_ID}} </div>
          <div class="flex flex-row text-xs"> 
            <div label="role-deadline" class="text-grey"> Apply by {{formatDate(listing.application_deadline)}}</div>
            <div class="flex items-center mx-2">
              <span class="bg-black h-1 w-1 rounded-full"></span>
            </div>
            <div label="role-applicants" class="font-bold text-green"> 11 applicants </div>
          </div>
        </div>
        <div class="grow"></div>
        <div>
          <div class="flex flex-row">
            <div class="grow"></div>
            <div :class="{'bg-green': checkOpen(listing), 'bg-red': !checkOpen(listing)}" class="me-5 text-xs px-4 py-1 rounded-full text-white">  
              <span v-if="checkOpen(listing)">Open</span>
              <span v-else>Closed</span>
            </div>
          </div>
          <div class="flex flex-row items-center text-yellow pt-3">
            <div class="font-bold">{{ listing.dept }}</div>
            <div label="role-department" class="flex bg-yellow mx-2 h-1 w-1 rounded-full"> </div>
            <div label="role-country">{{ listing.country }}</div>
          </div>
        </div>
      </li>
 
    </ul>
  </div>
</template>

<style></style>