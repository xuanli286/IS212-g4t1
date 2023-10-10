<script setup>
import axios from "axios";
import { ref } from "vue";
import { useRoleListingStore } from '@/store/useRoleListingStore';
import { storeToRefs } from 'pinia';
import { useConstantStore } from '@/store/useConstantStore';

const constStore = useConstantStore();
const { backend_url } = storeToRefs(constStore);
const roleListingStore = useRoleListingStore();
const roleListings = ref({})
const staffNames = ref({})

axios
  .get(`${backend_url.value}/openrolelisting`)
  .then((response) => {
    let receivedListings = response.data.data.rolelisting
    for (let listing of receivedListings) {
      for (let key in listing) {
        roleListings.value[key] = listing[key]
      }
    }
  })
  .catch(error => {
    if (error.response) {
      if (error.response.status === 404) {
        console.log("No open listings at this moment.");
      }
    }
  })

axios
  .get(`${backend_url.value}/closerolelisting`)
  .then((response) => {
    let receivedListings = response.data.data.rolelisting
    for (let listing of receivedListings) {
      for (let key in listing) {
        roleListings.value[key] = listing[key]
      }
    }
  })
  .catch(error => {
    if (error.response) {
      if (error.response.status === 404) {
        console.log("No closed listings at this moment.");
      }
    }
  })

axios
  .get(`${backend_url.value}/staff`)
  .then((response) => {
    let allStaff = response.data.data.staff
    for (let staff of allStaff) {
      for (let key in staff) {
        staffNames.value[key] = staff[key]
      }
    }
  })

function checkOpen(listing) {
  let today = new Date();
  let deadline = new Date(listing.application_deadline)
  if (deadline > today) {
    return true
  }

  return false
}

function formatDate(dateString) {
  let date = new Date(dateString)
  let day = date.getDate()
  let month = date.toLocaleString('default', { month: 'long' });
  let year = date.getFullYear()
  return `${day} ${month} ${year}`
}

const updateRoleListingId = (id) => {
  roleListingStore.setRoleListingId(id)
}

const getManagerName = (id) => {
  try {
    var FName = staffNames.value[id]["staff_FName"]
    var LName = staffNames.value[id]["staff_LName"][0]
  } catch (error) {

  }
  return `${FName} ${LName}.`
}

</script>

<template>
  <div class="bg-beige px-10 py-5">
    <div class="flex flex-row mx-64">
      <div class="flex flex-row grow py-20 text-xl font-serif text-center " id="roleListings">
        <div class="grow"></div>
        <h1 class="translate-x-[85px]">Manage Role Listing</h1>
        <div class="grow"></div>
      </div>
      <div class="flex items-center">
        <router-link id="addRoleListingButton" to="/addrolelisting"
          class="flex flex-row bg-yellow py-2 px-5 rounded-full text-white text-sm">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor"
            class="w-6 h-6 me-2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v6m3-3H9m12 0a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <div class="my-auto">Add Role Listing</div>
        </router-link>
      </div>
    </div>
    <ul class="mx-64 min-w-fit rolelisting-container">
      <li v-if="Object.keys(roleListings).length == 0" class="py-5 text-center">
        <div class="grow"></div>
        <div class="font-bold">No listings available!</div>
        <div class="grow"></div>
      </li>
      <li v-else v-for="(listing, id) in roleListings" :key="id"
        class="rolelisting-panel flex border-t py-5 hover:bg-grey-50">
        <router-link to="/specificrolelisting" @click=updateRoleListingId(id)>
          <div class="flex-none h-100">
            <div class="role-title text-yellow text-xl"> {{ listing.role_name }} </div>
            <div class="role-manager text-base"> Reporting Manager: {{ getManagerName(listing.manager_ID) }} </div>
            <div class="flex flex-row text-xs">
              <div class="role-deadline text-grey"> Apply by {{ formatDate(listing.application_deadline) }}</div>
              <div class="flex items-center mx-2">
                <span class="bg-black h-1 w-1 rounded-full"></span>
              </div>
              <div class="role-applicants font-bold text-green"> 11 applicants </div>
            </div>
          </div>
        </router-link>
        <div class="grow"></div>
        <div>
          <div class="flex flex-row">
            <div class="grow"></div>
            <div :class="{ 'bg-green': checkOpen(listing), 'bg-red': !checkOpen(listing) }"
              class="role-status me-5 text-xs px-4 py-1 rounded-full text-white">
              <span v-if="checkOpen(listing)">Open</span>
              <span v-else>Closed</span>
            </div>
          </div>
          <div class="flex flex-row items-center text-yellow pt-3">
            <div class="font-bold">{{ listing.dept }}</div>
            <div class="role-department flex bg-yellow mx-2 h-1 w-1 rounded-full"> </div>
            <div class="role-country">{{ listing.country }}</div>
          </div>
        </div>
      </li>

    </ul>
  </div>
</template>

<style></style>