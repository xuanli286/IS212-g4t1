<template>
  <div class="grid grid-cols-2">
    <div class="p-8">
      <img class="pt-8 pb-12" alt="logo" src="../assets/icons/logo.png">
      <h1 class="flex mb-14 text-4xl font-serif">Sign In</h1>
      <form class="space-y-4 md:space-y-6" action="#">
        <div>
            <label for="email" class="mb-2 text-sm font-medium text-black flex">Email</label>
            <input v-model="email" type="email" name="email" id="email" class="bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5" placeholder="name@company.com" required="">
        </div>
        <div>
            <label for="password" class="flex mb-2 text-sm font-medium text-black">Password</label>
            <input v-model="password" type="password" name="password" id="password" placeholder="••••••••" class="bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5" required="">
        </div>
        <button @click="submitForm" type="submit" class="bg-yellow hover:bg-yellow w-full text-white font-bold py-2 px-4 rounded">Sign in</button>
      </form>
    </div>
    <div class="p-0">
      <img class="object-contain" src="../assets/icons/loginpage.png" alt="">
    </div>
    
  </div>
  
</template>

<script>
// import axios from 'axios';

export default {
  name: 'HelloWorld',
  data() {
    return {
      email: "",
      password: ""
    }
  },
  methods: {
    submitForm() {
      // Gather user input data
      console.log(this.email)
      console.log(this.password)
      const email = this.email
      const password = this.password
  
      // Create a data object to send to the backend
      
      const formData = {
        "email": email,
        "password": password
      };
      console.log(formData)

      // Make a POST request to your backend API
      // axios.post('/api/login', formData)
      //   .then(response => {
      //     // Handle successful response from the backend
      //     console.log('Login successful:', response.data);
      //     // You can perform any necessary actions here, e.g., redirect the user to another page.
      //   })
      //   .catch(error => {
      //     // Handle error response from the backend
      //     console.error('Login failed:', error);
      //     // You can display an error message to the user or take other appropriate actions.
      //   });
    }
  }
}
</script>