<template>
  <div class="link-container">
    <div v-if="loading" class="loading">Loading...</div>
    <div v-else>
      <div v-if="link" class="link-display">
        <a :href="link" target="_blank">{{ link }}</a>
        <div class="actions">
          <button @click="toggleEdit" class="icon-button">
            <div v-if="!isEditing">✏️</div>
            <div v-if="isEditing">✅</div>
          </button>
          <button @click="deleteLink" class="icon-button">❌</button>
        </div>
      </div>
      <div v-else class="add-link">
          GitHub > <button @click="toggleEdit" class="icon-button">➕</button>
      </div>
      <div v-if="isEditing" class="edit-section">
        <input v-model="newLink" type="text" placeholder="Enter GitHub repository link" />
        <button @click="saveLink" class="save-button">Save</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      link: null,
      newLink: "",
      isEditing: false,
      loading: true,
    };
  },
  methods: {
    async fetchLink() {
      try {
        const response = await axios.get("http://127.0.0.1:5000/api/student/get_github_repo", {
          data: { student_id: JSON.parse(localStorage.getItem("user_info") || "{}").user_id, },
        });
        this.link = response.data.github_repo_link;
      } catch (error) {
        console.error("Error fetching link:", error);
      } finally {
        this.loading = false;
      }
    },
    toggleEdit() {
      this.newLink = this.link || "";
      this.isEditing = !this.isEditing;
    },
    async saveLink() {
      try {
        const endpoint = this.link ? "http://127.0.0.1:5000/api/student/update_github_repo" : "http://127.0.0.1:5000/api/student/link_github_repo";
        await axios.post(endpoint, {
          student_id: JSON.parse(localStorage.getItem("user_info") || "{}").user_id,
          github_repo_link: this.newLink,
        });
        this.link = this.newLink;
        this.isEditing = false;
      } catch (error) {
        console.error("Error saving link:", error);
      }
    },
    async deleteLink() {
      try {
        await axios.post("http://127.0.0.1:5000/api/student/delete_github_repo", {
          student_id: JSON.parse(localStorage.getItem("user_info") || "{}").user_id,
        });
        this.link = null;
      } catch (error) {
        console.error("Error deleting link:", error);
      }
    },
  },
  mounted() {
    this.fetchLink();
  },
};
</script>

<style scoped>
.link-container {
  display: flex;
  flex-direction: column;
  margin: 1rem 0;
  padding: 1rem;
  border: 1px solid #ccc;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.loading {
  text-align: center;
  color: gray;
}

.link-display,
.add-link {
  font-weight: bold;
  color: black;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.actions {
  display: flex;
  gap: 1rem;
}

.icon-button {
  background: #fff;
  border-radius: 50%;
  padding: 0.5rem;
  border: none;
  cursor: pointer;
}

.edit-section {
  margin-top: 0.5rem;
}

input {
  width: 80%;
  padding: 0.5rem;
  font-size: 1rem;
  border: 1px solid #ccc;
  border-radius: 4px;
  color: gray;
}

.save-button {
  padding: 0.5rem 1rem;
  margin-left: 0.5rem;
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.save-button:hover {
  background-color: #0056b3;
}
</style>