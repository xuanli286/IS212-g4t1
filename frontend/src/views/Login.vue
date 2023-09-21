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
            <input v-model="password" type="password" name="password" id="password" placeholder="••••••••" class="bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5" required="">
        </div>
        <button @click="submitForm" class="bg-yellow hover:bg-yellow w-full text-white font-bold py-2 px-4 rounded">Sign in</button>
        <span v-if="wrongMsg" class="text-red">Wrong Staff ID or password! Please re-enter your details. If you have any other issues, contact the administrator</span>
      </form>
    </div>
    <div class="p-0">
      <img class="object-contain" src="../assets/icons/loginpage.png" alt="">
    </div>
    
  </div>
  
</template>

<script>
// import axios from 'axios';
const get_staff_URL = "http://127.0.0.1:5000/staff";

export default {
  name: 'HelloWorld',
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
      console.log(this.staffId)
      console.log(this.password)
      fetch(`${get_staff_URL}/${this.staffId}`)
      .then((response) => {
                if (response.status === 404) {
                  this.wrongMsg = true;
                }
                return response.json();
              })
              .then((data) => {
                // console.log(data);
                if (data.code === 200) {
                  console.log(data.data[this.staffId])
                  const staffData = data.data[this.staffId]
                  const staffPassword = staffData['staff_password']
                  console.log(staffPassword)
                  if (this.password == staffPassword)
                  {
                    this.wrongMsg = false
                    this.user = {access_ID: staffData['access_ID'], staff_FName: staffData['staff_FName'], staff_LName: staffData['staff_LName']}
                      // {access_ID: 2, staff_FName: "Philip", staff_LName: "Lee"};
                    console.log("Success!", this.user)
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