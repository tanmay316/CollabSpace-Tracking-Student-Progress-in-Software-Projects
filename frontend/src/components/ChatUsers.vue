<!-- ChatUsers.vue -->
<template>
  <div class="chat-users">
    <h2>Chat</h2>
    <ul>
      <li v-for="user in users" :key="user.id" class="user-item" @click="navigateToChat(user)">
        <img :src="user.image || 'https://via.placeholder.com/40'" alt="User Image" class="user-image" />
        <div class="user-info">
          <p class="user-name">{{ user.name }}</p>
          <p class="user-last-msg">{{ user.lastMessage  }}</p>
        </div>
      </li>
    </ul>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';

const users = ref([]);
const userInfo = JSON.parse(localStorage.getItem('user_info'));
const currentUserId = userInfo ? userInfo.user_id : null; 

const router = useRouter();

const navigateToChat = (user) => {
  router.push({ name: 'chatWindow', params: { id: user.id } });
};

onMounted(async () => {
  try {
    const response = await axios.get(`http://127.0.0.1:5000/api/chat/users`, {
      params: {
        current_user_id: currentUserId
      }
    });
    users.value = response.data;
  } catch (error) {
    console.error("Error fetching users:", error);
  }
});
</script>

<style scoped>
h2 {
  color: gray;
  font-weight: bold;
  font-size: 1.5rem;
  margin-bottom: 1rem;
}

.chat-users {
  margin-top: 5rem;
  background-color: #fff;
  padding: 16px;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.user-item {
  display: flex;
  align-items: center;
  padding: 12px;
  margin-bottom: 10px;
  background-color: #f8fafc;
  border-radius: 8px;
  cursor: pointer;
  position: relative;
  transition: background-color 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
}

.user-item:hover {
  background-color: #f1f5f9;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.user-image {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  margin-right: 12px;
}

.user-info {
  flex-grow: 1;
}

.user-name {
  color: black;
  font-weight: bold;
}

.user-last-msg {
  color: gray;
  font-size: 0.9rem;
}
</style>
