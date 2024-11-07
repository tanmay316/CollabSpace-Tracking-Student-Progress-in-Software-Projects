<template>
  <div class="border">
  <h2>Register</h2>
  <div>
    <label for="firstName">First Name:</label>
    <input type="text" v-model="firstName" ><br><br>
    
    <label for="lastName">Last Name:</label>
    <input type="text" v-model="lastName" ><br><br>
    
    <label for="email">Email:</label>
    <input type="email" v-model="email" required><br><br>
    
    <label for="password">Password:</label>
    <input type="password" v-model="password" required><br><br>
    
    <label for="password">Confirm Password:</label>
    <input type="password" v-model="password2" required><br><br>

    <label for="role" style="margin-right: 1rem;">Role:</label>
    <select style="padding: 0.5rem;" class="form-control" id="role" v-model="selectedRole">
      <option value="student">Student</option>
      <option value="ta">TA</option>
      <option value="admin">Admin</option>
      <option value="instructor">Instructor</option>
    </select><br><br>
    
    <button @click="register()">Register</button>
  </div>
    <br>
  <p>
  Already have an account? <RouterLink to="/login"> <button>Login</button> </RouterLink>
  </p>
</div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      selectedRole:'user'
    };
  },
  mounted() {

  },
  methods: {
    register() {
      const newUser = {
        firstName: this.firstName,
        lastName: this.lastName,
        email: this.email,
        password: this.password,
        role: this.selectedRole
      };
      if(this.password===this.password2){
        axios.post('http://127.0.0.1:4000/register', newUser,{
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
          }
        })
        .then(() => {
          this.firstName = '';
          this.lastName = '';
          this.email = '';
          this.password = '';
          this.$router.push('/login');
          })
          .catch(error => {
            console.error('Error adding new user:', error);
          });
        }else alert('password do not match')
    }
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
  color: black;
  font-weight: bold;
}

input[type='text'],
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
  color: black;
}
</style>
