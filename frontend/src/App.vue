<script setup>
import { RouterLink, RouterView } from 'vue-router'
import Navbar from './components/Navbar.vue';
import AiChatIcon from './components/AiChatIcon.vue';
</script>

<template>
  <Navbar/> 
  <RouterView />
  <AiChatIcon/>
</template>