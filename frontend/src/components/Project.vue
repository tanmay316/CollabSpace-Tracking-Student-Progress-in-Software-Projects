<template>
    <div class="container">
      <div class="header"><h2>Software Engineering Project</h2></div>
      <div class="content">
        <div class="grid">

          <div class="project-card">
            <div class="card-header">
              <h3>
                <RouterLink to="/milestones">Milestones</RouterLink>
              </h3>
              <a
                class="badge"
                href="https://github.com/anigaut/soft-engg-project-sep-2024-se-sep-10"
                target="_blank"
                rel="noreferrer"
                >GitHub</a
              >
            </div>
            <div class="card-body">
              <div v-if="loading">Loading milestones...</div>
              <div v-else-if="error">{{ error }}</div>
              <div v-else>
                <div
                  v-for="milestone in milestones"
                  :key="milestone.id"
                  class="milestones"
                >
                  <span v-if="role === 'student'">{{ getMilestoneStatus(milestone) }}</span> {{ milestone.title }}
                </div>
              </div>
            </div>
          </div>

          <div class="project-card">
            <div class="card-header">
              <h3>
                <RouterLink to="/mentorship">
                  <a href="" target="_blank" rel="noreferrer">Mentorship Sessions</a>
              </RouterLink>
            </h3>
            </div>
            <div class="card-body">
              <div>
                <p>Get mentorship from industry experts to learn frameworks and libraries for this project and beyond!</p>
              </div>
            </div>
          </div>
        </div>

        <div v-if="(role === 'student' && vivaSlots && vivaSlots.length > 0) || role === 'ta' || role === 'instructor'" class="project-card">
            <div class="card-header">
              <h3>
                Viva Slots
              </h3>
              <span class="badge">Open</span>
            </div>
            <div class="card-body">
              <div class="slots">

                <div v-if="role === 'ta' || role === 'instructor'" class="slot-container">
                  <div class="slot-block2">
                    <label for="slotDate">Slot Date:</label>
                    <input id="slotDate" v-model="slotDate" type="date" class="input-field" />
                  </div>
                  <div class="slot-block2">
                    <label for="slotTime">Slot Time:</label>
                    <input id="slotTime" v-model="slotTime" type="time" class="input-field" />
                  </div>
                  <div @click="createVivaSlot" class="viva-icon">+ Create Viva Slot</div>
                </div>

                <div class="slot-container">
                  <div v-if="loading">Loading viva slots...</div>
                  <div v-else-if="error">{{ error }}</div>
                  <div v-else>
                    <div v-for="slot in vivaSlots" :key="slot.id" class="slot-block">
                      <div v-if="role === 'ta' || role === 'instructor'" class="slot-block2">
                        <input
                          v-model="slot.slot_date"
                          class="viva-date-icon"
                          type="date"
                          :placeholder="slot.slot_date"
                        />
                        <input
                          v-model="slot.slot_time"
                          class="viva-time-icon"
                          type="time"
                          :placeholder="slot.slot_time"
                        />
                        <div v-if="slot.status === 'available'" class="viva-icon" @click="updateVivaSlot(slot)">✏️</div>
                        <div class="viva-icon" @click="deleteVivaSlot(slot.id)">❌</div>
                      </div>

                      <div v-if="slot.status === 'available' && role === 'student'" class="slot-block1">
                        <div
                          class="slot"
                          @click="bookVivaSlot(slot.id)"
                        >
                          {{ slot.slot_date }} {{ formatTime(slot.slot_time) }}
                        </div>
                      </div>

                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

      </div>
    </div>
  </template>

<script setup>

const formatTime = (time) => {
  const [hours, minutes] = time.split(':');
  const formattedHours = hours % 12 || 12; // Convert to 12-hour format
  const period = hours < 12 ? 'AM' : 'PM';
  return `${formattedHours}:${minutes} ${period}`;
};

import { ref, onMounted } from "vue";
import axios from "axios";

const milestones = ref([]);

const fetchMilestones = async () => {
  try {
    const milestoneResponse = await axios.get("http://127.0.0.1:5000/api/student/milestones");
    const milestoneData = milestoneResponse.data.milestones;

    for (const milestone of milestoneData) {
      try {
        const submissionResponse = await axios.get(
          `http://127.0.0.1:5000/api/student/get_submission/${milestone.id}`
        );
        const submissionDetails = submissionResponse.data.submission_details;

        const currentDate = new Date();
        const deadlineDate = new Date(milestone.deadline);

        if (submissionDetails.github_branch_link) {
          milestone.status = currentDate <= deadlineDate ? "🟢 " : "🔴 ";
        } else {
          milestone.status = currentDate <= deadlineDate ? "⚪️ " : "🔴 ";
        }
      } catch (error) {
        const currentDate = new Date();
        const deadlineDate = new Date(milestone.deadline);

        milestone.status = currentDate > deadlineDate ? "🔴 " : "⚪️ ";
      }
    }

    milestones.value = milestoneData;
  } catch (err) {
    error.value = "Failed to load milestones.";
    console.error(err.response?.data || err.message);
  } finally {
    loading.value = false;
  }
};

const getMilestoneStatus = (milestone) => {
  return milestone.status || "⚪️ ";
};

fetchMilestones();

const vivaSlots = ref([]);
const loading = ref(false);
const error = ref(null);

const role = JSON.parse(localStorage.getItem("user_info"))?.role || "";

const fetchVivaSlots = async () => {
  loading.value = true;
  error.value = null;
  try {
    const response = await axios.get("http://127.0.0.1:5000/api/ta/api/viva_slots");
    vivaSlots.value = response.data;
  } catch (err) {
    error.value = "Failed to load viva slots.";
    console.error(err.response?.data || err.message);
  } finally {
    loading.value = false;
  }
};

const slotDate = ref('');
const slotTime = ref('');

const createVivaSlot = async () => {
  try {
    const userInfo = JSON.parse(localStorage.getItem('user_info') || '{}');
    const taId = userInfo.user_id;

    if (!taId || !slotDate.value || !slotTime.value) {
      alert("All fields are required.");
      return;
    }

    const formattedTime = `${slotTime.value}:00`;

    const response = await axios.post("http://127.0.0.1:5000/api/ta/api/viva_slots", {
      ta_id: taId,
      slot_date: slotDate.value,
      slot_time: formattedTime,
    });

    slotDate.value = '';
    slotTime.value = '';
    await fetchVivaSlots();
  } catch (err) {
    alert("Failed to create viva slot.");
    console.error(err.response?.data || err.message);
  }
};

const updateVivaSlot = async (slot) => {
  try {
    const response = await axios.post(
      `http://127.0.0.1:5000/api/ta/api/viva_slots/${slot.id}`,
      {
        slot_date: slot.slot_date,
        slot_time: `${slot.slot_time}:00`,
        status: slot.status,
      }
    );
    alert(response.data.message);
    await fetchVivaSlots();
  } catch (err) {
    alert("Failed to update viva slot.");
    console.error(err.response?.data || err.message);
  }
};

const deleteVivaSlot = async (slotId) => {
  try {
    const response = await axios.delete(`http://127.0.0.1:5000/api/ta/api/viva_slots/${slotId}`);
    await fetchVivaSlots();
  } catch (err) {
    alert("Failed to delete viva slot.");
    console.error(err.response?.data || err.message);
  }
};

const bookVivaSlot = async (slotId) => {
  if (!confirm('Do you want to book this viva slot?')) return;

  try {
    const response = await axios.post(`http://127.0.0.1:5000/api/student/book_viva_slot/${slotId}`);

    await fetchVivaSlots();
  } catch (err) {
    alert('Failed to book viva slot.');
    console.error(err.response?.data || err.message);
  }
};

onMounted(fetchMilestones);
onMounted(fetchVivaSlots);
</script>
  
  <style scoped>
  .slot-block1, .slot-block2{
    gap: 0.5rem;
    display: flex;
    padding: 0.5rem;
    justify-content: space-between;
  }

  .slot-block{
    margin: 0.5rem;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    border-radius: 0.5rem;
  }

  .slot-block:hover{
    cursor: pointer;
    scale: 1.05;
    transition: transform 0.2s ease-in-out;
  }

  .slot-container{
    padding: 0.5rem;
    margin: 0.5rem;
    display: flex;
    flex-direction: column;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  }

  h2 {
  color: gray;
  font-weight: bold;
  font-size: 1.5rem;
  margin-bottom: 1rem;
  }

  .slots{
    color: #000;
    display: flex;
    padding: 0.5rem;
  }
  
  .slot{
    align-content: center;
    color: #000;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    border-radius: 8px;
    padding: 0.5rem;
  }

  .create-slot{
    color: #000;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    border-radius: 8px;
    padding: 0.5rem;
  }

  .create-slot:hover{
    cursor: pointer;
    transform: scale(1.05);
    background-color: #06b6d4;
  }

  .viva-date-icon{
    padding: 0.5rem;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  }

  .viva-icon{
    padding: 1rem;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  }

  .viva-icon:hover{
    cursor: pointer;
    background-color: #06b6d4;
  }
  
  .slot:hover{
    cursor: pointer;
    transform: scale(1.05);
    background-color: #10b981;
  }
  
  .container {
    background-color: #f3f4f6;
    padding: 24px;
    margin-top: 5rem;
  }

  .milestones{
    color: black;
  }
  
  .header {
    text-align: center;
    font-size: 1.5rem;
    color: #000;
    padding-bottom: 48px;
  }
  
  .content {
    max-width: 64rem;
    margin: 0 auto;
  }
  
  .grid {
    display: grid;
    grid-template-columns: 1fr;
    gap: 24px;
    margin-bottom: 2rem;
  }
  
  @media (min-width: 640px) {
    .grid {
      grid-template-columns: repeat(2, 1fr);
    }
  }

  .project-card {
    background-color: #fff;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    border-radius: 8px;
    /* transition: transform 0.2s ease-in-out; */
    overflow: hidden;
  }
  
  /* .project-card:hover {
    transform: scale(1.05);
  } */
  
  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 16px;
    border-bottom: 1px solid #e5e7eb;
  }
  
  .card-header h3 {
    font-size: 1.25rem;
    font-weight: 600;
    color: #111827;
  }
  
  .card-header a {
    text-decoration: none;
    color: inherit;
  }
  
  .badge {
    background-color: #1f2937;
    font-size: 0.875rem;
    font-weight: 500;
    padding: 4px 8px;
    border-radius: 9999px;
  }
  
  .card-body {
    padding: 16px;
  }
  
  .card-body p {
    color: #4b5563;
    font-size: 1rem;
  }
  
  .card-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 16px;
    border-top: 1px solid #e5e7eb;
  }
  
  .technologies {
    display: flex;
    align-items: center;
  }
  
  .p1-dot,
  .p2-dot {
    width: 12px;
    height: 12px;
    border-radius: 50%;
    margin-right: 8px;
  }
  
  .p1-dot {
    background-color: #06b6d4;
  }
  
  .p2-dot {
    background-color: #13cd73;
  }
  
  .label {
    font-size: 0.875rem;
    color: #374151;
    margin-right: 16px;
  }
  
  .stats {
    color: #6b7280;
    font-size: 0.875rem;
  }
  </style>
  