<template>
    <div class="container">
        <div class="sidebar">
            <h1>Upload</h1>
            <input type="file" ref="fileInput" multiple />
            <button @click="uploadFiles">Submit & Process</button>
        </div>

        <div class="main-content">
            <h1>Chat and Summarize</h1>
            <div class="messages">
                <div v-for="(message, index) in messages" :key="index" :class="['message', message.type]">
                    <template v-if="message.type === 'bot' || message.type === 'summary'">
                        <div v-html="formatStructuredResponse(message.content)"></div>
                    </template>
                    <template v-else>
                        <strong>{{ message.role }}:</strong> {{ message.content }}
                    </template>
                </div>
            </div>

            <div class="chat-input">
                <input type="text" v-model="question" placeholder="Ask a question or summarize..."
                    @keypress.enter="askQuestion" />
                <button @click="askQuestion">Ask</button>
                <button @click="summarizeFile">Summarize</button>
            </div>
        </div>
    </div>
</template>

<script>
const API_BASE_URL = "http://127.0.0.1:5000/api/pdf";

export default {
    data() {
        return {
            question: "",
            messages: [],
        };
    },
    methods: {
        async uploadFiles() {
            const files = this.$refs.fileInput.files;
            const formData = new FormData();

            for (const file of files) {
                formData.append("files", file);
            }

            this.addMessage("System", "Processing files...", "system");
            try {
                const response = await fetch(`${API_BASE_URL}/upload`, {
                    method: "POST",
                    body: formData,
                });
                const result = await response.json();
                this.addMessage("System", result.message, "system");
            } catch (error) {
                console.error("Error uploading files:", error);
                this.addMessage("System", "Error processing files!", "system");
            }
        },
        async askQuestion() {
            if (!this.question) {
                this.addMessage("System", "Please enter a question.", "system");
                return;
            }

            this.addMessage("You", this.question, "user");
            try {
                const response = await fetch(`${API_BASE_URL}/ask`, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({ question: this.question }),
                });
                const result = await response.json();
                this.addMessage("Bot", result.response, "bot");
            } catch (error) {
                console.error("Error asking question:", error);
                this.addMessage("System", "Error getting the response!", "system");
            }

            this.question = "";
        },
        async summarizeFile() {
            this.addMessage("System", "Summarizing...", "system");
            try {
                const response = await fetch(`${API_BASE_URL}/summarize`, {
                    method: "POST",
                });
                const result = await response.json();
                this.addMessage("Summary", result.summary, "summary");
            } catch (error) {
                console.error("Error summarizing:", error);
                this.addMessage("System", "Error generating the summary!", "system");
            }
        },
        addMessage(role, content, type) {
            this.messages.push({ role, content, type });
            this.$nextTick(() => {
                const messagesDiv = this.$el.querySelector(".messages");
                messagesDiv.scrollTop = messagesDiv.scrollHeight;
            });
        },
        formatStructuredResponse(response) {
            const sections = response.split("**").filter((section) => section.trim() !== "");
            let htmlContent = "";

            sections.forEach((section) => {
                if (section.includes(":")) {
                    const [title, ...content] = section.split(":");
                    htmlContent += `<h3>${title.trim()}</h3>`;
                    if (content.length) {
                        const bulletPoints = content
                            .join(":")
                            .split("*")
                            .filter((item) => item.trim() !== "");
                        bulletPoints.forEach((item) => {
                            htmlContent += `<li>${item.trim()}</li>`;
                        });
                    }
                } else {
                    const bulletPoints = section.split("*").filter((item) => item.trim() !== "");
                    bulletPoints.forEach((item) => {
                        htmlContent += `<li>${item.trim()}</li>`;
                    });
                }
            });

            return `<div>${htmlContent}</div>`;
        },
    },
};
</script>

<style scoped>
.container {
    display: flex;
    height: calc(100vh - 70px);
    margin: 5rem;
}

h1{
    color: gray;
    font-weight: bold;
    font-size: 1.5rem;
    margin-bottom: 1rem;
}

.sidebar {
    width: 300px;
    background-color: #f8f9fa;
    color: black;
    padding: 20px;
    box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1);
}

.sidebar h1 {
    text-align: center;
    margin-bottom: 20px;
}

.sidebar button {
    width: 100%;
    padding: 10px;
    margin-top: 10px;
    border: none;
    background-color: #007bff;
    color: white;
    border-radius: 5px;
    cursor: pointer;
}

.sidebar button:hover {
    background-color: #0056b3;
}

.main-content {
    flex-grow: 1;
    padding: 20px;
    background-color: white;
    color: black;
    display: flex;
    flex-direction: column;
    border-left: 1px solid #ddd;
}

.messages {
    flex-grow: 1;
    overflow-y: auto;
    padding: 10px;
    border-radius: 5px;
    background-color: #f8f8f8;
    border: 1px solid #ddd;
}

.message {
    margin-bottom: 15px;
    padding: 10px;
    border-radius: 5px;
}

.message.system {
    background-color: #e9ecef;
}

.message.user {
    background-color: #d1ecf1;
}

.message.bot {
    background-color: #f8d7da;
}

.message.summary {
    background-color: #fff3cd;
}

.chat-input {
    gap: 0.5rem;
    display: flex;
    padding: 0.5rem 0;
    justify-content: space-between;
    align-items: baseline;
}

.chat-input input {
    flex-grow: 1;
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 5px;
}

.chat-input button {
    background-color: #007bff;
    color: white;
    border: none;
    padding: 10px 15px;
    border-radius: 5px;
    cursor: pointer;
}

.chat-input button:hover {
    background-color: #0056b3;
}
</style>
