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
                  <span>{{ getMilestoneStatus(milestone.deadline) }}</span> {{ milestone.title }}
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

        <div class="project-card">
            <div class="card-header">
              <h3>
                Viva Slots
              </h3>
              <span class="badge">Open</span>
            </div>
            <div class="card-body">
              <div class="slots">

                <div class="slot-container">
                  <div class="slot-block2">
                    <input class="viva-date-icon" type="date">
                  </div>
                  <div class="slot-block1">
                    <div class="create-slot" @click="createVivaSlot()">+ Viva Slot</div>
                  </div>
                </div>

                <div class="slot-container">
                  <div v-if="loading">Loading viva slots...</div>
                  <div v-else-if="error">{{ error }}</div>
                  <div v-else>
                    <div v-for="slot in vivaSlots" :key="slot.id" class="slot-block">
                      <div class="slot-block1">
                        <div class="slot" @click="bookVivaSlot(slot.id)" v-if="slot.status === 'available'">
                          {{ slot.slot_date }} {{ slot.slot_time }}
                        </div>
                        <div class="slot" v-else>
                          {{ slot.slot_date }} {{ slot.slot_time }} ({{ slot.status }})
                        </div>
                        <div class="viva-icon" @click="deleteVivaSlot(slot.id)">❌</div>
                      </div>
                      <div class="slot-block2">
                        <input class="viva-date-icon" type="date">
                        <div class="viva-icon" @click="updateVivaSlot(slot)">✏️</div>
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
import { ref, computed, onMounted } from "vue";
import axios from "axios";

const milestones = ref([]);

const fetchMilestones = async () => {
  try {
    const response = await axios.get("http://127.0.0.1:5000/api/student/milestones");
    milestones.value = response.data.milestones;
  } catch (err) {
    error.value = "Failed to load milestones.";
    console.error(err.response?.data || err.message);
  } finally {
    loading.value = false;
  }
};

const getMilestoneStatus = (deadline) => {
  const currentDate = new Date();
  const deadlineDate = new Date(deadline);

  if (currentDate < deadlineDate) {
    return "⚪️";
  } else if (currentDate.toDateString() === deadlineDate.toDateString()) {
    return "🟢";
  } else {
    return "🔴";
  }
};

const vivaSlots = ref([]);
const loading = ref(false);
const error = ref(null);

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

const createVivaSlot = async () => {
  try {
    const taId = prompt("Enter TA ID:");
    const slotDate = prompt("Enter slot date (YYYY-MM-DD):");
    const slotTime = prompt("Enter slot time (HH:MM:SS):");

    if (!taId || !slotDate || !slotTime) {
      alert("All fields are required.");
      return;
    }

    const response = await axios.post("http://127.0.0.1:5000/api/ta/api/viva_slots", {
      ta_id: taId,
      slot_date: slotDate,
      slot_time: slotTime,
    });
    alert(response.data.message);
    await fetchVivaSlots();
  } catch (err) {
    alert("Failed to create viva slot.");
    console.error(err.response?.data || err.message);
  }
};

const updateVivaSlot = async (slot) => {
  try {
    const slotDate = prompt("Enter new slot date (YYYY-MM-DD):", slot.slot_date);
    const slotTime = prompt("Enter new slot time (HH:MM:SS):", slot.slot_time);
    const status = prompt("Enter new status:", slot.status);

    const response = await axios.post(`http://127.0.0.1:5000/api/ta/api/viva_slots/${slot.id}`, {
      slot_date: slotDate,
      slot_time: slotTime,
      status: status,
    });
    alert(response.data.message);
    await fetchVivaSlots();
  } catch (err) {
    alert("Failed to update viva slot.");
    console.error(err.response?.data || err.message);
  }
};

const deleteVivaSlot = async (slotId) => {
  if (!confirm("Are you sure you want to delete this slot?")) return;

  try {
    const response = await axios.delete(`http://127.0.0.1:5000/api/ta/api/viva_slots/${slotId}`);
    alert(response.data.message);
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
    alert(response.data.message);

    // Reload the viva slots after booking
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
  