<template>
  <div class="border">
    <h2>Login</h2>

    <div>
      <label for="email">Email:</label>
      <input type="email" v-model="email" required /><br /><br />

      <label for="password">Password:</label>
      <input type="password" v-model="password" required /><br /><br />

      <button @click="login">Login</button>
    </div>

    <p>
      Don't have an account? 
      <router-link to="/register">
        <button>Register</button>
      </router-link>
    </p>
    <br />

    <div v-if="errorMessage" class="alert">
      {{ errorMessage }}
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';

const email = ref('');
const password = ref('');
const errorMessage = ref('');
const router = useRouter();

const login = async () => {
  if (!email.value || !password.value) {
    errorMessage.value = 'Email and Password are required.';
    return;
  }

  try {
    const response = await axios.post('http://127.0.0.1:5000/api/auth/login', {
      email: email.value,
      password: password.value,
    });

    alert(response.data.message || 'Login successful!');

    // Save access token and user info to local storage
    const { access_token, admin_info } = response.data;
    localStorage.setItem('access_token', access_token);
    localStorage.setItem('user_info', JSON.stringify(admin_info));

    // Redirect based on user role
    const userRole = admin_info.role.toLowerCase();
    console.log(userRole)
    router.push('/')
    // if (userRole === 'admin') {
    //   router.push('/admin/dashboard');
    // } else if (userRole === 'ta') {
    //   router.push('/ta/dashboard');
    // } else if (userRole === 'instructor') {
    //   router.push('/instructor/dashboard');
    // } else {
    //   router.push('/student/dashboard');
    // }
  } catch (error) {
    errorMessage.value =
      error.response?.data?.message || 'Login failed. Please check your credentials.';
    console.error(error.response || error.message);
  }
};
</script>
  
<style>

.border{
    padding: 2rem;
    background-color: #fff;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    border-radius: 8px;
    margin-top: 5rem;
}

h2 {
  color: gray;
  font-weight: bold;
  font-size: 1.5rem;
  margin-bottom: 1rem;
}

label {
  font-weight: bold;
  color: black;
}

input[type='email'],
input[type='password'] {
  width: 100%;
  padding: 0.5rem;
  margin-bottom: 1rem;
}

button {
  padding: 0.5rem 1rem;
  background-color: #007bff;
  color: #fff;
  border: none;
  cursor: pointer;
}

p{
  margin-top: 1rem;
}
</style>
  