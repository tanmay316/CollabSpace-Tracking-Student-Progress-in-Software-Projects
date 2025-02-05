<template>
  <nav class="navbar">
    <div class="navbar-left">
      <RouterLink to="/" class="brand">CollabSpace</RouterLink>
    </div>

    <div class="navbar-right" :class="{ active: isNavbarOpen }">
      <RouterLink v-if="!isLoggedIn" to="/login" class="nav-item">Login</RouterLink>
      <RouterLink v-if="!isLoggedIn" to="/register" class="nav-item">Register</RouterLink>
      <RouterLink v-if="isLoggedIn" to="/" class="nav-item" @click="logout">Logout</RouterLink>
      <RouterLink v-if="isLoggedIn" to="/chatUsers" class="nav-item">Chat</RouterLink>
      <RouterLink v-if="role === 'instructor' || role === 'TA'" to="/summaryai" class="nav-item">Summarizer</RouterLink>
      <RouterLink v-if="role === 'ta'" to="/plagiarism-check" class="nav-item">Plagiarism</RouterLink>
      <RouterLink v-if="role === 'instructor' || role === 'TA'" to="/students" class="nav-item">Students</RouterLink>
    </div>

    <input type="checkbox" class="menu" v-model="isNavbarOpen" />
  </nav>
</template>

<script setup>

import { ref, onMounted } from 'vue';
import { useRouter, RouterLink } from 'vue-router';

import axios from 'axios';

const role = ref(null);
const isLoggedIn = ref(false);

onMounted(() => {
  const userInfo = localStorage.getItem('user_info');
  if (userInfo) {
    const parsedInfo = JSON.parse(userInfo);
    role.value = parsedInfo.role;
    isLoggedIn.value = true;
  } else {
    isLoggedIn.value = false;
  }
});

const router = useRouter();
const isNavbarOpen = ref(false); // Reactive state to track navbar visibility

const logout = async () => {
  try {
    const response = await axios.post("http://127.0.0.1:5000/api/auth/logout", {}, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem("access_token")}`,
      },
    });

    alert(response.data.message || "Logged out successfully!");

    role.value = null;
    localStorage.removeItem("access_token");
    localStorage.removeItem("user_info");

    // router.push("/");
    window.location.href = '/';
  } catch (error) {
    console.error("Logout failed:", error.response || error.message);
    alert(error.response?.data?.message || "An error occurred while logging out.");
  }
};
</script>

<style scoped>
.navbar {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #1f2937;
  color: white;
  padding: 10px 24px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  z-index: 1000;
}

/* Branding on the left */
.navbar-left .brand {
  font-size: 1.5rem;
  font-weight: bold;
  color: #ffffff;
  text-decoration: none;
}

/* Navbar links on the right */
.navbar-right {
  display: flex;
  gap: 16px;
  transition: all 0.3s ease-in-out;
}

.navbar-right.active {
  display: flex;
  flex-direction: column;
  gap: 8px;
  position: absolute;
  top: 100%;
  right: 10px;
  background-color: #1f2937;
  padding: 10px;
  border-radius: 5px;
}

.nav-item {
  color: #ffffff;
  text-decoration: none;
  font-size: 1rem;
  transition: color 0.2s ease-in-out;
}

.nav-item:hover {
  color: #a3e635;
  /* Light green on hover */
}

/* Body margin adjustment to avoid navbar overlap */
body {
  margin: 0;
  padding-top: 60px;
}

/* Hamburger icon - Custom design */
.menu {
  --s: 20px;
  /* Control the size */
  --c: white;
  /* Hamburger icon color */

  height: var(--s);
  aspect-ratio: 1;
  border: none;
  padding: 0;
  border-inline: calc(var(--s)/2) solid transparent;
  box-sizing: content-box;
  --_g1: linear-gradient(var(--c) 20%, #0000 0 80%, var(--c) 0) no-repeat content-box border-box;
  --_g2: radial-gradient(circle closest-side at 50% 12.5%, var(--c) 95%, #0000) repeat-y content-box border-box;
  background:
    var(--_g2) left var(--_p, 0px) top,
    var(--_g1) left calc(var(--s)/10 + var(--_p, 0px)) top,
    var(--_g2) right var(--_p, 0px) top,
    var(--_g1) right calc(var(--s)/10 + var(--_p, 0px)) top;
  background-size:
    20% 80%,
    40% 100%;
  position: relative;
  clip-path: inset(0 25%);
  cursor: pointer;
  transition:
    background-position .3s var(--_s, .3s),
    clip-path 0s var(--_s, .6s);
  -webkit-appearance: none;
  -moz-appearance: none;
  appearance: none;
}

.menu:before,
.menu:after {
  content: "";
  position: absolute;
  border-radius: var(--s);
  inset: 40% 0;
  background: var(--c);
  transition: transform .3s calc(.3s - var(--_s, .3s));
}

.menu:checked {
  clip-path: inset(0);
  --_p: calc(-1*var(--s));
  --_s: 0s;
}

.menu:checked:before {
  transform: rotate(45deg);
}

.menu:checked:after {
  transform: rotate(-45deg);
  background: rgb(255, 255, 255);
  /* Cross color change */
}

.menu:focus-visible {
  clip-path: none;
  border: none;
  outline: 2px solid var(--c);
  outline-offset: 5px;
}

/* Media query for small screens */
@media (max-width: 768px) {

  /* Hide navbar links on small screens */
  .navbar-right {
    display: none;
    /* Hide navbar links on small screens */
  }

  /* Show hamburger icon on small screens */
  .menu {
    display: block;
  }

  /* Show navbar links when hamburger is clicked */
  .menu:checked+.navbar-right {
    display: flex;
    flex-direction: column;
    gap: 8px;
    position: absolute;
    top: 100%;
    right: 10px;
    background-color: #1f2937;
    padding: 10px;
    border-radius: 5px;
  }
}

/* Hide hamburger icon on larger screens */
@media (min-width: 769px) {
  .menu {
    display: none;
    /* Hide hamburger icon on larger screens */
  }
}
</style>
