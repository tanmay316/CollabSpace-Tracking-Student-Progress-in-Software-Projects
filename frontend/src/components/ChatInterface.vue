<template>
  <div class="chat-interface">
    <div class="messages">
      <div 
        v-for="(message, index) in messages" 
        :key="index" 
        :class="{'sent': message.sent, 'received': !message.sent}">
        <p>{{ message.text }}</p>
      </div>
    </div>
    <div class="message-input">
      <input 
        v-model="newMessage" 
        @keyup.enter="sendMessage" 
        placeholder="Type a message..." 
      />
      <button @click="sendMessage">Send</button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const messages = ref([
  { text: 'Hello!', sent: true },
  { text: 'Hi! How are you?', sent: false },
]);

const newMessage = ref('');

const sendMessage = () => {
  if (newMessage.value.trim()) {
    messages.value.push({ text: newMessage.value, sent: true });
    newMessage.value = '';
  }
};
</script>

<style scoped>
.chat-interface {
  box-shadow:0 4px 6px rgba(0, 0, 0, 0.1);
  margin-top: 5rem;
  display: flex;
  flex-direction: column;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 16px;
  background-color: #fff;
  height: 75vh;
}

.messages {
  flex-grow: 1;
  overflow-y: auto;
}

.sent,
.received{
  padding: 0.5rem;
  border-bottom: 1px solid #e5e7eb;
}

.messages .sent {
  text-align: right;
  color: #10b981;
}

.messages .received {
  text-align: left;
  color: #4b5563;
}

.message-input {
  display: flex;
  gap: 8px;
  margin-top: 16px;
}

.message-input input {
  flex: 1;
  padding: 10px;
  border-radius: 8px;
  border: 1px solid #ddd;
}

.message-input button {
  background-color: #10b981;
  color: white;
  padding: 10px 16px;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.2s ease-in-out;
}

.message-input button:hover {
  background-color: #34d399;
}
</style>
