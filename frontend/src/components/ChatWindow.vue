<!-- src/components/ChatWindow.vue -->
<template>
  <div class="chat-window">
    <!-- Chat Header -->
    <header class="chat-header">
      <div class="user-info">
        <img class="user-avatar" :src="otherUser.avatarUrl || '/default-avatar.jpg'" alt="User Avatar" />
        <div class="user-details">
          <h3>{{ otherUser.name }}</h3>
          <span>{{ otherUser.role }}</span>
        </div>
      </div>
      <!-- Optional: Add action buttons like settings or options here -->
      <div class="header-actions">
        <button class="action-button">
          &#9881; <!-- Gear Icon as a placeholder -->
        </button>
      </div>
    </header>

    <!-- Chat Messages -->
    <ul class="chat-messages">
      <li v-for="msg in messages" :key="msg.id" :class="['message', msg.isSent ? 'sent' : 'received']">
        <div class="message-bubble">
          <p>{{ msg.message }}</p>
          <small>{{ formatTimestamp(msg.timestamp) }}</small>
        </div>
      </li>
    </ul>

    <!-- Chat Input -->
    <div class="chat-input">
      <input v-model="newMessage" type="text" placeholder="Type your message..." @keyup.enter="sendMessage" />
      <button @click="sendMessage" :disabled="!newMessage.trim()">
        Send
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, nextTick } from 'vue';
import axios from 'axios';
import { useRoute } from 'vue-router';

// Helper function to format timestamps
const formatTimestamp = (timestamp) => {
  const date = new Date(timestamp);
  return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
};

// Reactive references
const route = useRoute();
const senderId = 1; // Replace with the logged-in user's ID

// Get receiverId from route params
const receiverId = ref(route.params.id);

// Fetch other user details if needed
const otherUser = ref({ name: 'Loading...', role: 'Loading...', avatarUrl: '' });

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
      params: { sender_id: senderId, receiver_id: receiverId.value },
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
      params: { current_user_id: senderId },
    });
    const user = response.data.find((u) => u.id === parseInt(receiverId.value));
    if (user) {
      otherUser.value = { name: user.name, role: user.role, avatarUrl: user.avatarUrl };
    } else {
      otherUser.value = { name: 'Unknown', role: 'Unknown', avatarUrl: '/default-avatar.jpg' };
    }
  } catch (error) {
    console.error('Error fetching other user:', error);
  }
};

// Watch for route changes to update receiverId
watch(
  () => route.params.id,
  (newId) => {
    receiverId.value = newId;
    fetchMessages();
    fetchOtherUser();
  }
);

// Initial fetch
onMounted(() => {
  fetchMessages();
  fetchOtherUser();
});

// Function to send a message
const sendMessage = async () => {
  if (newMessage.value.trim() === '') return;
  try {
    const messageData = {
      sender_id: senderId,
      receiver_id: receiverId.value,
      message: newMessage.value,
    };
    const response = await axios.post('http://127.0.0.1:5000/api/chat/send_message', messageData);
    if (response.data.message === 'Message sent successfully') {
      messages.value.push({
        sender_id: senderId,
        receiver_id: receiverId.value,
        message: newMessage.value,
        timestamp: new Date().toISOString(),
        isSent: true,
      });
      newMessage.value = ''; // Clear the input field
      scrollToBottom();
    }
  } catch (error) {
    console.error('Error sending message:', error);
  }
};

// Function to scroll to the latest message
const scrollToBottom = () => {
  nextTick(() => {
    const container = document.querySelector('.chat-messages');
    if (container) {
      container.scrollTop = container.scrollHeight;
    }
  });
};
</script>

<style scoped>
.chat-window {
  margin: 50px auto 0 auto;
  display: flex;
  flex-direction: column;
  height: 92vh;
  background: linear-gradient(135deg, #080808, #2a0231, #220e49);
  font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
  color: #ffffff;
}

/* Chat Header */
.chat-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  background: rgba(0, 0, 0, 0.3);
  /* Semi-transparent overlay for better readability */
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
}

.user-info {
  display: flex;
  align-items: center;
}

.user-avatar {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  object-fit: cover;
  margin-right: 12px;
  border: 2px solid #ffffff;
}

.user-details h3 {
  margin: 0;
  font-size: 18px;
  font-weight: bold;
  color: #ffffff;
}

.user-details span {
  font-size: 14px;
  color: #dddddd;
}

.header-actions .action-button {
  background: rgba(255, 255, 255, 0.2);
  border: none;
  font-size: 20px;
  cursor: pointer;
  color: #ffffff;
  padding: 8px;
  border-radius: 50%;
  transition: background 0.3s;
}

.header-actions .action-button:hover {
  background: rgba(255, 255, 255, 0.4);
}

/* Chat Messages */
.chat-messages {
  flex: 1;
  padding: 16px;
  overflow-y: auto;
  background: rgba(0, 0, 0, 0.1);
  /* Light overlay for message readability */
}

.chat-messages li {
  display: flex;
  margin-bottom: 12px;
}

.chat-messages li.sent {
  justify-content: flex-end;
}

.chat-messages li.received {
  justify-content: flex-start;
}

.message-bubble {
  max-width: 60%;
  padding: 10px 14px;
  border-radius: 18px;
  background: rgba(255, 255, 255, 0.2);
  position: relative;
  font-size: 14px;
  color: #ffffff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.chat-messages li.sent .message-bubble {
  background: linear-gradient(45deg, #6228d7,#2ac7ee);
  color: #010000;
}

.chat-messages li.received .message-bubble {
  background: linear-gradient(45deg, #f9ce34, #ee2a7b);
  color: #020202;
}

.message-bubble small {
  display: block;
  font-size: 10px;
  color: #0a0a0a;
  margin-top: 4px;
  text-align: right;
}

/* Chat Input */
.chat-input {
  display: flex;
  align-items: center;
  padding: 16px;
  background: rgba(0, 0, 0, 0.3);
  /* Semi-transparent overlay for consistency */
  border-top: 1px solid rgba(255, 255, 255, 0.2);
}

.chat-input input {
  flex: 1;
  padding: 10px 16px;
  border: none;
  border-radius: 24px;
  font-size: 14px;
  outline: none;
  background: rgba(255, 255, 255, 0.2);
  color: #ffffff;
  transition: background 0.3s;
}

.chat-input input::placeholder {
  color: #cccccc;
}

.chat-input input:focus {
  background: rgba(255, 255, 255, 0.3);
}

.chat-input button {
  margin-left: 12px;
  padding: 10px 20px;
  background: linear-gradient(45deg, #ee2a7b, #6228d7);
  border: none;
  border-radius: 24px;
  color: #ffffff;
  font-size: 14px;
  cursor: pointer;
  transition: background 0.3s, transform 0.2s;
}

.chat-input button:hover {
  background: linear-gradient(45deg, #6228d7, #ee2a7b);
  transform: translateY(-2px);
}

.chat-input button:disabled {
  background: rgba(238, 42, 123, 0.6);
  cursor: not-allowed;
}

/* Scrollbar Styling for WebKit Browsers */
.chat-messages::-webkit-scrollbar {
  width: 8px;
}

.chat-messages::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 4px;
}

.chat-messages::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.3);
  border-radius: 4px;
}

.chat-messages::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 255, 255, 0.5);
}

/* Responsive Design */
@media (max-width: 768px) {

  .chat-header,
  .chat-input {
    padding: 12px;
  }

  .user-avatar {
    width: 40px;
    height: 40px;
    margin-right: 8px;
  }

  .user-details h3 {
    font-size: 16px;
  }

  .user-details span {
    font-size: 12px;
  }

  .message-bubble {
    max-width: 80%;
    font-size: 13px;
  }

  .chat-input input {
    font-size: 13px;
  }

  .chat-input button {
    padding: 8px 16px;
    font-size: 12px;
  }
}
</style>
