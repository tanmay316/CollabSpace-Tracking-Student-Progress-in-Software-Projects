<template>
  <div class="container">
    <div class="sidebar">
      <h1>CollabSpace AI Chatbot</h1>
      <form @submit.prevent="handleSubmit">
        <label for="repolink">GitHub Repo Link:</label>
        <input type="text" v-model="repolink" placeholder="Enter GitHub Repo Link" />

        <label for="files">Upload Code or PDF Files:</label>
        <input type="file" ref="fileInput" multiple @change="handleFileUpload" />

        <button type="submit">Submit</button>
      </form>
      <div class="status">{{ statusMessage }}</div>
    </div>

    <div class="main-content">
      <h2 style="color: black;">Chat with Code File and GitHub Repo</h2>
      <div class="chat-section" ref="chatBox">
        <p v-for="(msg, index) in chatMessages" :key="index">
          <strong>{{ msg.role }}:</strong> {{ msg.content }}
        </p>
      </div>
      <div class="chat-input">
        <input type="text" v-model="userMessage" placeholder="Ask about Repo or Files..." />
        <button @click="sendMessage">Ask</button>
      </div>

      <h2 style="color: black;">Ask and Debug</h2>
      <div class="chat-section" ref="directChatBox">
        <p v-for="(msg, index) in directMessages" :key="index">
          <strong>{{ msg.role }}:</strong> {{ msg.content }}
        </p>
      </div>
      <div class="chat-input">
        <input type="text" v-model="directMessage" placeholder="Chat directly with AI..." />
        <button @click="sendDirectMessage">Ask</button>
      </div>
    </div>
  </div>
</template>

<script>
const API_BASE_URL = "http://localhost:5000/api/rag"; // Ensure this points to your backend

export default {
  data() {
    return {
      repolink: "",
      files: [],
      userMessage: "",
      directMessage: "",
      statusMessage: "",
      chatMessages: [],
      directMessages: [],
    };
  },
  methods: {
    handleFileUpload(event) {
      this.files = Array.from(event.target.files);
    },
    async handleSubmit() {
      const formData = new FormData();
      if (this.repolink) formData.append("repolink", this.repolink);
      this.files.forEach((file) => formData.append("files", file));

      this.statusMessage = "Processing...";
      try {
        const response = await fetch(`${API_BASE_URL}/submit`, {
          method: "POST",
          body: formData,
        });
        const result = await response.json();
        if (response.ok) {
          this.statusMessage = "Ready! You can now ask questions.";
        } else {
          this.statusMessage = result.error || "An error occurred.";
        }
      } catch (error) {
        this.statusMessage = "Failed to process the request.";
      }
    },
    async sendMessage() {
      if (!this.userMessage) {
        alert("Please enter a question.");
        return;
      }

      const message = { role: "You", content: this.userMessage };
      this.chatMessages.push(message);

      try {
        const response = await fetch(`${API_BASE_URL}/chat`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ message: this.userMessage }),
        });
        const result = await response.json();
        if (response.ok) {
          this.chatMessages.push({ role: "Assistant", content: result.response });
        } else {
          alert(result.error || "An error occurred.");
        }
      } catch {
        alert("Failed to fetch response.");
      }

      this.userMessage = "";
      this.scrollToBottom(this.$refs.chatBox);
    },
    async sendDirectMessage() {
      if (!this.directMessage) {
        alert("Please enter a message.");
        return;
      }

      const message = { role: "You", content: this.directMessage };
      this.directMessages.push(message);

      try {
        const response = await fetch(`${API_BASE_URL}/direct_chat`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ message: this.directMessage }),
        });
        const result = await response.json();
        if (response.ok) {
          this.directMessages.push({ role: "AI", content: result.response });
        } else {
          alert(result.error || "An error occurred.");
        }
      } catch {
        alert("Failed to fetch response.");
      }

      this.directMessage = "";
      this.scrollToBottom(this.$refs.directChatBox);
    },
    scrollToBottom(element) {
      element.scrollTop = element.scrollHeight;
    },
  },
};
</script>

<style scoped>
.container {
  display: flex;
  height: calc(100vh - 60px);
  /* Adjusted height to account for navbar */
  margin-top: 50px;
  /* Add gap below navbar */
}

.sidebar {
  width: 300px;
  background-color: #2c3e50;
  color: white;
  padding: 20px;
  box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1);
  overflow-y: auto;
}

.sidebar h1 {
  text-align: center;
  margin-bottom: 20px;
}

.sidebar label {
  display: block;
  margin-top: 10px;
  font-weight: bold;
}

.sidebar input[type="text"],
.sidebar input[type="file"] {
  width: 100%;
  padding: 10px;
  margin: 10px 0;
  border: none;
  border-radius: 5px;
  box-sizing: border-box;
}

.sidebar button {
  width: 100%;
  background-color: #3498db;
  color: white;
  padding: 10px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.sidebar button:hover {
  background-color: #2980b9;
}

.main-content {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  padding: 10px;
  overflow-y: auto;
}

.chat-section {
  flex-grow: 1;
  border: 1px solid #0b0a0a;
  border-radius: 5px;
  padding: 10px;
  background-color: #8d8d8f;
  overflow-y: auto;
  max-height: 200px;
  /* Reduced height for better fit */
  margin-bottom: 10px;
}

.chat-input {
  display: flex;
  gap: 10px;
}

.chat-input input {
  flex-grow: 1;
  padding: 10px;
  border: 1px solid #b91818;
  border-radius: 5px;
}

.chat-input button {
  background-color: #3498db;
  color: white;
  border: none;
  padding: 10px 15px;
  border-radius: 5px;
  cursor: pointer;
}

.chat-input button:hover {
  background-color: #2980b9;
}

.status {
  margin-bottom: 10px;
  font-style: italic;
  color: #888;
}
</style>
