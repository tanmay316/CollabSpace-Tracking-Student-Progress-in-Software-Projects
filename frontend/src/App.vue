<script setup>
import { RouterView } from 'vue-router'
import Navbar from './components/Navbar.vue';
import AiChatIcon from './components/AIChatIcon.vue';

import { ref, onMounted } from 'vue';

const role = ref(null);

onMounted(() => {
  const userInfo = localStorage.getItem('user_info');
  role.value = userInfo ? JSON.parse(userInfo).role : null;
});

</script>

<template>
  <Navbar/> 
  <RouterView />
  <AiChatIcon v-if="role === 'student'"/>
</template>