<!-- ChatWindow.vue -->
<template>
  <div class="chat-window">
    <header class="chat-header">
      <h3>{{ otherUser.name }}</h3>
      <span>{{ otherUser.role }}</span>
    </header>
    <ul class="chat-messages">
      <li v-for="msg in messages" :key="msg.id" :class="{ sent: msg.isSent, received: !msg.isSent }">
        <p>{{ msg.message }}</p>
        <small>{{ msg.timestamp }}</small>
      </li>
    </ul>
    <div class="chat-input">
      <input v-model="newMessage" placeholder="Type your message..." />
      <button @click="sendMessage">Send</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import axios from 'axios';
import { useRoute } from 'vue-router';

const route = useRoute();
const senderId = 1; // Replace with the logged-in user's ID, ideally fetched from auth

// Get receiverId from route params
const receiverId = ref(route.params.id);

// Fetch other user details if needed
const otherUser = ref({ name: 'Loading...', role: 'Loading...' });

// Fetch messages
const messages = ref([]);
const newMessage = ref('');

// Function to fetch messages
const fetchMessages = async () => {
  try {
    if (!senderId || !receiverId.value) {
      console.error('Sender ID and Receiver ID are required');
      return;
    }

    const response = await axios.get('http://127.0.0.1:5000/api/chat/get_messages', {
      params: {
        sender_id: senderId,
        receiver_id: receiverId.value
      }
    });

    messages.value = response.data.messages;
  } catch (error) {
    console.error('Error fetching messages:', error);
  }
};

// Function to fetch other user details
const fetchOtherUser = async () => {
  try {
    const response = await axios.get('http://127.0.0.1:5000/api/chat/users', {
      params: {
        current_user_id: senderId
      }
    });
    const user = response.data.find(u => u.id === parseInt(receiverId.value));
    if (user) {
      otherUser.value = { name: user.name, role: user.role };
    } else {
      otherUser.value = { name: 'Unknown', role: 'Unknown' };
    }
  } catch (error) {
    console.error('Error fetching other user:', error);
  }
};

// Watch for route changes to update receiverId
watch(() => route.params.id, (newId) => {
  receiverId.value = newId;
  fetchMessages();
  fetchOtherUser();
});

// Initial fetch
onMounted(() => {
  fetchMessages();
  fetchOtherUser();
});

// Function to send a message
const sendMessage = async () => {
  try {
    if (newMessage.value.trim() === '') return;

    const messageData = {
      sender_id: senderId,
      receiver_id: receiverId.value,
      message: newMessage.value
    };

    const response = await axios.post('http://127.0.0.1:5000/api/chat/send_message', messageData);

    if (response.data.message === "Message sent successfully") {
      messages.value.push({
        sender_id: senderId,
        receiver_id: receiverId.value,
        message: newMessage.value,
        timestamp: new Date().toISOString(),
        isSent: true
      });
      newMessage.value = ''; // Clear the input field
    }
  } catch (error) {
    console.error('Error sending message:', error);
  }
};
</script>

<style scoped>
.chat-window {
  padding: 0.5rem;
  margin: 0.5rem;
  display: flex;
  flex-direction: column;
  height: 100%;
  color: black;
}

.chat-header {
  display: flex;
  justify-content: space-between;
  padding: 16px;
  border-bottom: 1px solid #060606;
  color: black;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
  color: black;
}

.chat-messages li {
  margin-bottom: 10px;
  color: black;
}

.chat-messages li.sent {
  text-align: right;
  color: black;
}

.chat-messages li.received {
  text-align: left;
  color: black;
}

.chat-input {
  display: flex;
  padding: 16px;
  border-top: 1px solid #070707;
  color: black;
}

.chat-input input {
  flex: 1;
  margin-right: 8px;
  color: black;
}
</style>
