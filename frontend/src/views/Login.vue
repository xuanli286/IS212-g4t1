<template>
  <div class="grid grid-cols-2">
    <div class="p-8">
      <img class="pt-8 pb-12" alt="logo" src="../assets/icons/logo.png">
      <h1 class="flex mb-14 text-4xl font-serif">Sign In</h1>
      <form class="space-y-4 md:space-y-6" action="#">
        <div>
            <label for="staffId" class="mb-2 text-sm font-medium text-black flex">Staff ID</label>
            <input v-model="staffId" name="staffId" id="staffId" class="bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5" placeholder="" required="">
        </div>
        <div>
            <label for="password" class="flex mb-2 text-sm font-medium text-black">Password</label>
            <input v-model="password" type="password" name="password" id="password" class="bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5" required="">
        </div>
        <button @click="submitForm" id="login" class="bg-yellow hover:bg-yellow-50 w-full text-white font-bold py-2 px-4 rounded">Sign in</button>
        <span v-if="wrongMsg" class="text-red" id="errorMessage">Wrong Staff ID or password! Please re-enter your details. If you have any other issues, contact the administrator</span>
      </form>
    </div>
    <div class="p-0">
      <img class="object-contain" src="../assets/icons/loginpage.png" alt="">
    </div>
    
  </div>
  
</template>

<script>
// import axios from 'axios';
import { useUserStore } from '../store/useUserStore';
import { useConstantStore } from '@/store/useConstantStore';

export default {
  name: 'HelloWorld',
  setup() {
    const backend_url = useConstantStore().backend_url;

    const userStore = useUserStore();

    return { backend_url, userStore}
  },
  data() {
    return {
      staffId: "",
      password: "",
      user: {},
      wrongMsg: false
    }
  },
  methods: {
    async submitForm(event) {
      event.preventDefault();
      // Gather user input data
      fetch(`${this.backend_url}/staff/${this.staffId}`)
      .then((response) => {
                if (response.status === 404) {
                  this.wrongMsg = true;
                }
                return response.json();
              })
              .then((data) => {
                if (data.code === 200) {
                  const staffData = data.data[this.staffId]
                  const staffPassword = staffData['staff_password']
                  if (this.password == staffPassword)
                  {
                    this.wrongMsg = false
                    this.user = {access_ID: staffData['access_ID'], staff_FName: staffData['staff_FName'], staff_LName: staffData['staff_LName']}

                    this.userStore.setUser({
                      access_ID: staffData['access_ID'],
                      staff_FName: staffData['staff_FName'],
                      staff_LName: staffData['staff_LName'],
                      staff_dept: staffData['dept'],
                      staff_country: staffData['country'],
                      staff_email: staffData['email'],
                      staff_ID: this.staffId
                    });
                    // Redirect to the home page
                    
                    this.$router.push({ name: 'Home' });
                  }
                  else
                  {
                    this.wrongMsg = true
                    // alert("Wrong Staff ID or Password! Please reenter.")
                  }
                }
              })
              .catch((error) => {
                console.log(error);
                this.wrongMsg = true
                // alert("Wrong Staff ID or Password! Please reenter.")
              });
    }
  }
}
</script>