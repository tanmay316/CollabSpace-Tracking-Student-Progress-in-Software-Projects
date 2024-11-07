<script setup>
import ChatUsers from '../components/ChatUsers.vue';
</script>

<template>
  <div class="chat-users">
    <main>
      <ChatUsers/>
    </main>
  </div>
</template>

<style>
@media (min-width: 1024px) {
  .chat-users {
    width: 100vh;
    min-height: 100vh;
    align-items: center;
  }
}
</style>
