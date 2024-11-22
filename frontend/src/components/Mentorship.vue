<template>
    <div class="mc">
        <h2>Mentorship Courses</h2>
        <div class="mentorship-session">
            <img src="https://via.placeholder.com/100" alt="Mentor Image" class="mentor-image" />
            <div class="session-details">
            <div class="same-line">
                <h3 class="session-title">Title: </h3>
                <input type="text">
            </div>
            <div class="same-line">
                <p class="mentor-name">Mentor Name: </p>
                <input type="text">
            </div>
            <div class="same-line">
                <p class="session-description">Description: </p>
                <input type="text">
            </div>
            <div class="same-line">
                <p class="session-amount">Amount: </p>
                <input type="text">
            </div>
            <div class="create-mentorship">+ Mentorship</div>
            </div>
        </div>
        <div>
    <div v-if="loading">Loading sessions...</div>
    <div v-else-if="error">{{ error }}</div>
    <div v-else>
      <div
        v-for="session in mentorshipSessions"
        :key="session.id"
        class="mentorship-session"
      >
        <img
          src="https://via.placeholder.com/100"
          alt="Mentor Image"
          class="mentor-image"
        />
        <div class="session-details">
          <div class="space-head">
            <div>
              <h3 class="session-title">{{ session.description }}</h3>
              <input
                type="text"
                v-model="session.description"
                class="input-field"
              />
            </div>
            <div class="icons" @click="deleteSession(session.id)">❌</div>
          </div>
          <div>
            <p class="mentor-name">{{ session.mentor_name }}</p>
            <input
              type="text"
              v-model="session.mentor_name"
              class="input-field"
            />
          </div>
          <div>
            <p class="session-description">{{ session.description }}</p>
            <input
              type="text"
              v-model="session.description"
              class="input-field"
            />
          </div>
          <div>
            <p class="session-amount">${{ session.price }}</p>
            <input
              type="text"
              v-model="session.price"
              class="input-field"
            />
          </div>
          <div class="align-icon">
            <div class="icons" @click="updateSession(session)">✏️</div>
          </div>
        </div>
      </div>
    </div>
  </div>
        <!-- <div class="mentorship-session">
            <img src="https://via.placeholder.com/100" alt="Mentor Image" class="mentor-image" />
            <div class="session-details">
            <div class="space-head">
                <div>
                    <h3 class="session-title">Mentorship Course 1</h3>
                    <input type="text">
                </div>
                <div class="icons">❌</div>
            </div>
            <div>
                <p class="mentor-name">Anurag</p>
                <input type="text">
            </div>
            <div>
                <p class="session-description">
                    This is a detailed description of the mentorship session, covering the topics that will be addressed.
                </p>
                <input type="text">
            </div>
            <div>
                <p class="session-amount">$008</p>
                <input type="text">
            </div>
            <div class="align-icon">
                <div class="icons">✏️</div>
            </div>
            </div>
        </div> -->
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

const mentorshipSessions = ref([]);
const loading = ref(true);
const error = ref("");

const fetchMentorshipSessions = async () => {
  try {
    const response = await axios.get('http://127.0.0.1:5000/api/student/mentorship_sessions');
    mentorshipSessions.value = response.data;
  } catch (err) {
    error.value = 'Failed to load mentorship sessions.';
    console.error(err.response?.data || err.message);
  } finally {
    loading.value = false;
  }
};

const updateSession = async (session) => {
  try {
    const response = await axios.post(
      `http://127.0.0.1:5000/mentorship_sessions/${session.id}`,
      {
        description: session.description,
        mentor_name: session.mentor_name,
        price: session.price,
      }
    );
    alert(response.data.message || 'Session updated successfully.');
  } catch (err) {
    alert('Failed to update session.');
    console.error(err.response?.data || err.message);
  }
};

const deleteSession = async (sessionId) => {
  if (!confirm('Are you sure you want to delete this session?')) return;

  try {
    const response = await axios.delete(
      `http://127.0.0.1:5000/mentorship_sessions/${sessionId}`
    );
    alert(response.data.message || 'Session deleted successfully.');
    mentorshipSessions.value = mentorshipSessions.value.filter(
      (session) => session.id !== sessionId
    );
  } catch (err) {
    alert('Failed to delete session.');
    console.error(err.response?.data || err.message);
  }
};

onMounted(fetchMentorshipSessions);
</script>

  
<style scoped>
.align-icon{
display: flex;
justify-content: end;
}

.space-head{
display: flex;
align-items: baseline;
justify-content: space-between;
}

.icons{
padding: 1rem;
box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.icons:hover{
cursor: pointer;
}

h2 {
color: gray;
font-weight: bold;
font-size: 1.5rem;
margin-bottom: 1rem;
}

.create-mentorship{
color: #000;
box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
border-radius: 8px;
width: fit-content;
margin: 1rem;
padding: 0.5rem;
}

.create-mentorship:hover{
cursor: pointer;
transform: scale(1.05);
background-color: #06b6d4;
}

.same-line{
align-items: baseline;
gap:1rem;
display: flex;
padding: 0.5rem;
border-radius: 4px;
}

.mc{
margin-top: 5rem;
display: flex;
flex-direction: column;
}

.mentorship-session {
display: flex;
align-items: flex-start;
background-color: #fff;
padding: 16px;
border-radius: 8px;
box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
margin-bottom: 16px;
}

.mentor-image {
width: 100px;
height: 100px;
object-fit: cover;
border-radius: 8px;
margin-right: 16px;
}

.session-details {
flex: 1;
}

.session-title {
color: #717171;
font-size: 1.25rem;
font-weight: bold;
margin-bottom: 8px;
}

.mentor-name {
font-size: 1rem;
font-weight: 600;
margin-bottom: 8px;
color: #1f2937; /* Dark text */
}

.session-description {
font-size: 0.9rem;
color: #4b5563; /* Medium text */
margin-bottom: 12px;
}

.session-amount {
font-size: 1.1rem;
font-weight: bold;
color: #10b981; /* Green text */
}
</style>
