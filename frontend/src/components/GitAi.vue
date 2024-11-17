<template>
    <div class="container">
        <div class="sidebar">
            <h1>CollabSpace AI Chatbot</h1>
            <form @submit.prevent="submitForm">
                <label for="repolink">GitHub Repo Link:</label>
                <input type="text" v-model="repolink" id="repolink" name="repolink">

                <label for="files">Upload Code or PDF Files:</label>
                <input type="file" id="files" multiple @change="handleFileUpload">

                <button type="submit">Submit</button>
            </form>
            <div class="status">{{ statusMessage }}</div>
        </div>

        <div class="main-content">
            <h2>Chat with code file and GitHub Repo</h2>
            <div class="chat-section" ref="chatBox">
                <p v-for="(message, index) in chatMessages" :key="index">
                    <strong>{{ message.sender }}:</strong> {{ message.text }}
                </p>
            </div>
            <div class="chat-input">
                <input type="text" v-model="userMessage" placeholder="Ask about Repo or Files...">
                <button @click="sendMessage">Ask</button>
            </div>

            <h2>Ask and Debug</h2>
            <div class="chat-section" ref="directChatBox">
                <p v-for="(message, index) in directChatMessages" :key="index">
                    <strong>{{ message.sender }}:</strong> {{ message.text }}
                </p>
            </div>
            <div class="chat-input">
                <input type="text" v-model="directMessage" placeholder="Chat directly with AI...">
                <button @click="sendDirectMessage">Ask</button>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'GitAi',
    data() {
        return {
            repolink: '',
            files: [],
            statusMessage: '',
            userMessage: '',
            directMessage: '',
            chatMessages: [],
            directChatMessages: []
        };
    },
    methods: {
        handleFileUpload(event) {
            this.files = Array.from(event.target.files);
        },
        async submitForm() {
            const formData = new FormData();
            formData.append('repolink', this.repolink);
            this.files.forEach(file => {
                formData.append('files', file);
            });

            this.statusMessage = 'Processing...';

            try {
                const response = await fetch('/api/rag/submit', {
                    method: 'POST',
                    body: formData
                });
                const result = await response.json();

                if (response.ok) {
                    this.statusMessage = 'Ready! You can now ask questions.';
                } else {
                    this.statusMessage = result.error;
                }
            } catch (error) {
                this.statusMessage = 'Error submitting form.';
            }
        },
        async sendMessage() {
            if (!this.userMessage) {
                alert('Please enter a question.');
                return;
            }

            const message = this.userMessage;
            this.chatMessages.push({ sender: 'You', text: message });

            try {
                const response = await fetch('/api/rag/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message })
                });
                const result = await response.json();

                if (response.ok) {
                    this.chatMessages.push({ sender: 'Assistant', text: result.response });
                } else {
                    alert(result.error);
                }
            } catch (error) {
                alert('Error sending message.');
            } finally {
                this.userMessage = '';
                this.$nextTick(() => {
                    this.$refs.chatBox.scrollTop = this.$refs.chatBox.scrollHeight;
                });
            }
        },
        async sendDirectMessage() {
            if (!this.directMessage) {
                alert('Please enter a message.');
                return;
            }

            const message = this.directMessage;
            this.directChatMessages.push({ sender: 'You', text: message });

            try {
                const response = await fetch('/api/rag/direct_chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message })
                });
                const result = await response.json();

                if (response.ok) {
                    this.directChatMessages.push({ sender: 'AI', text: result.response });
                } else {
                    alert(result.error);
                }
            } catch (error) {
                alert('Error sending message.');
            } finally {
                this.directMessage = '';
                this.$nextTick(() => {
                    this.$refs.directChatBox.scrollTop = this.$refs.directChatBox.scrollHeight;
                });
            }
        }
    }
};
</script>

<style scoped>
.container {
    display: flex;
    height: 100vh;
    font-family: Arial, sans-serif;
    background-color: #f4f4f9;
    color: #333;
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
    padding: 20px;
}

.chat-section {
    flex-grow: 1;
    border: 1px solid #ccc;
    border-radius: 5px;
    padding: 10px;
    background-color: #fff;
    overflow-y: auto;
    max-height: 300px;
    margin-bottom: 10px;
}

.chat-input {
    display: flex;
    gap: 10px;
}

.chat-input input {
    flex-grow: 1;
    padding: 10px;
    border: 1px solid #ccc;
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
