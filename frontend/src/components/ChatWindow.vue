<template>
  <div id="chat" class="chat-window">
    <header class="chat-header">
      <div class="user-info">
        <RouterLink to="/chatUsers"><div class="icon"> く </div></RouterLink>
        <div class="user-details">
          <h3>{{ otherUser.name }}</h3>
          <span>{{ otherUser.role }}</span>
        </div>
      </div>
    </header>

    <ul class="chat-messages">
      <li v-for="msg in messages" :key="msg.id" :class="['message', msg.isSent ? 'sent' : 'received']">
        <div class="message-bubble">
          <p>{{ msg.message }}</p>
          <small>{{ formatTimestamp(msg.timestamp) }}</small>
        </div>
      </li>
    </ul>

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

const formatTimestamp = (timestamp) => {
  const date = new Date(timestamp);
  return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
};

const route = useRoute();
const users = ref([]);
const userInfo = JSON.parse(localStorage.getItem('user_info'));
const senderId = userInfo ? userInfo.user_id : null;

const receiverId = ref(route.params.id);

const otherUser = ref({ name: 'Loading...', role: 'Loading...', avatarUrl: '' });

const messages = ref([]);
const newMessage = ref('');

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

watch(
  () => route.params.id,
  (newId) => {
    receiverId.value = newId;
    fetchMessages();
    fetchOtherUser();
  }
);

onMounted(() => {
  fetchMessages();
  fetchOtherUser();
});

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
      newMessage.value = '';
      scrollToBottom();
    }
  } catch (error) {
    console.error('Error sending message:', error);
  }
};

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
  margin-top: 5rem;
  max-width: 700px;
  background-color: #fff;
  padding: 16px;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  height: 92vh;
}

.chat-header {
  display: flex;
  align-items: center;
  border-bottom: 1px solid #e5e7eb;
  padding-bottom: 12px;
  margin-bottom: 16px;
}

.icon {
  color: black;
  border-radius: 50%;
  padding: 0.5rem;
  cursor: pointer;
}

.user-info {
  display: flex;
  gap: 12px;
  align-items: center;
}

.user-details h3 {
  font-size: 1.2rem;
  color: #111827;
  margin: 0;
}

.user-details span {
  font-size: 0.9rem;
  color: #6b7280;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
  background-color: #f9fafb;
  border-radius: 8px;
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
  max-width: 70%;
  padding: 12px;
  border-radius: 12px;
  background-color: #e5e7eb;
  position: relative;
  font-size: 14px;
  color: #1f2937;
}

.chat-messages li.sent .message-bubble {
  background-color: #34d399;
  color: #ffffff;
}

.chat-messages li.received .message-bubble {
  background-color: #f3f4f6;
}

.message-bubble small {
  display: block;
  font-size: 0.75rem;
  color: #6b7280;
  margin-top: 4px;
  text-align: right;
}

.chat-input {
  display: flex;
  align-items: center;
  padding: 12px 16px;
  background-color: #f9fafb;
  border-radius: 8px;
  margin-top: 16px;
}

.chat-input input {
  flex: 1;
  padding: 10px 16px;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  outline: none;
  font-size: 14px;
  color: #374151;
}

.chat-input input::placeholder {
  color: #9ca3af;
}

.chat-input button {
  margin-left: 12px;
  padding: 10px 20px;
  background-color: #3b82f6;
  border: none;
  border-radius: 8px;
  color: #ffffff;
  font-size: 14px;
  cursor: pointer;
}

.chat-input button:hover {
  background-color: #2563eb;
}

/* Scrollbar Styling for Chat Messages */
.chat-messages::-webkit-scrollbar {
  width: 6px;
}

.chat-messages::-webkit-scrollbar-thumb {
  background: rgba(156, 163, 175, 0.5);
  border-radius: 3px;
}

.chat-messages::-webkit-scrollbar-thumb:hover {
  background: rgba(156, 163, 175, 0.7);
}

@media (max-width: 768px) {
  .chat-header {
    flex-wrap: wrap;
  }

  .user-details h3 {
    font-size: 1rem;
  }

  .user-details span {
    font-size: 0.8rem;
  }

  .message-bubble {
    font-size: 13px;
  }

  .chat-input input {
    font-size: 13px;
  }

  .chat-input button {
    font-size: 13px;
  }
}
</style>