<template>
  <div class="submission-container">
    <div class="submission-header">Milestone Submissions</div>
    <div class="submission-grid">
      <div 
        v-for="submission in submissions" 
        :key="submission.id" 
        class="submission-card"
      >
        <div class="card-icon">
          <div class="circle-icon">{{ getInitials(submission.title) }}</div>
        </div>
        <div class="card-content">
          <h3>{{ submission.title }}</h3>
          <p>{{ submission.description }}</p>
          <div class="feedback-section">
            <input 
              v-model="submission.feedback" 
              placeholder="Enter submission link." 
              class="link-input"
            />
            <button @click="sendFeedback(submission.id)">Submission Link</button>
          </div>
          <div class="feedback-section">
            <input 
              v-model="submission.feedback" 
              placeholder="Enter feedback..." 
              class="feedback-input"
            />
            <button @click="sendFeedback(submission.id)">Send Feedback</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const submissions = ref([
  {
    id: 1,
    title: 'CRUD Operations Implementation',
    description: 'Submission includes backend and frontend integration for CRUD.',
    feedback: ''
  },
  {
    id: 2,
    title: 'UI Design Submission',
    description: 'Completed UI components for the dashboard.',
    feedback: ''
  },
  {
    id: 3,
    title: 'Testing and Debugging',
    description: 'Includes test cases and debugging report.',
    feedback: ''
  }
]);

const sendFeedback = (id) => {
  const submission = submissions.value.find((s) => s.id === id);
  if (submission.feedback.trim()) {
    alert(`Feedback sent for "${submission.title}": ${submission.feedback}`);
    submission.feedback = ''; // Clear feedback field after sending
  } else {
    alert('Please enter feedback before sending.');
  }
};

const getInitials = (title) => {
  return title
    .split(' ')
    .map((word) => word[0])
    .join('')
    .toUpperCase()
    .slice(0, 2);
};
</script>

<style scoped>
h3{
  color: black;
}
.submission-container {
  background-color: #f3f4f6;
}

.submission-header {
  margin-top: 4rem;
  color: gray;
  margin-bottom: 3rem;
  text-align: center;
  font-size: 1.5rem;
  font-weight: bold;
}

.submission-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 2rem;
}

@media (min-width: 640px) {
  .submission-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

.submission-card {
  display: flex;
  align-items: center;
  background-color: #ffffff;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  overflow: hidden;
  padding: 16px;
}

.card-icon {
  margin-right: 16px;
}

.circle-icon {
  width: 50px;
  height: 50px;
  background-color: #e5e7eb;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
  font-weight: bold;
  color: #111827;
}

.card-content {
  flex: 1;
}

.card-content h3 {
  font-size: 1.25rem;
  margin-bottom: 8px;
  font-weight: 600;
}

.card-content p {
  font-size: 0.875rem;
  margin-bottom: 12px;
  color: #6b7280;
}

.feedback-section {
  display: flex;
  gap: 8px;
  align-items: center;
}

.feedback-input {
  flex: 1;
  padding: 8px;
  border-radius: 4px;
  border: 1px solid #d1d5db;
}

.link-input {
  flex: 1;
  padding: 8px;
  border-radius: 4px;
  border: 1px solid #d1d5db;
}

.feedback-input:focus {
  outline: none;
  border-color: #2563eb;
}

button {
  background-color: #2563eb;
  color: white;
  padding: 8px 12px;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.2s ease-in-out;
}

button:hover {
  background-color: #1d4ed8;
}
</style>
