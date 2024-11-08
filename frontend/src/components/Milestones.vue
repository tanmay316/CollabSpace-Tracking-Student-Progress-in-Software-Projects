<template>
    <div class="container">
      <div class="header">Milestones</div>
      <div class="content">
        <RouterLink to='/submission'>
        <div class="grid">
          <div 
            v-for="milestone in milestones" 
            :key="milestone.id" 
            class="milestone-card" 
            :class="{
              'completed': milestone.status === 'completed',
              'pending': milestone.status === 'pending',
              'incomplete': milestone.status === 'incomplete'
            }"
          >
            <div class="card-header">
              <h3>{{ milestone.title }}</h3>
              <span :class="statusClass(milestone.status)">
                {{ milestone.status }}
              </span>
            </div>
            <div class="card-body">
              <p>{{ milestone.description }}</p>
            </div>
          </div>
        </div>
      </RouterLink>
      </div>
    </div>
  </template>
  
  <script setup>
  const milestones = [
    {
      id: 0,
      title: 'Milestone 1',
      description: 'CRUD Operations.',
      status: 'pending'
    },
    {
      id: 1,
      title: 'Milestone 2',
      description: 'Setting up the project repository and structure.',
      status: 'completed'
    },
    {
      id: 2,
      title: 'Milestone 3',
      description: 'Implementing the user interface and frontend logic.',
      status: 'incomplete'
    },
    {
      id: 3,
      title: 'Milestone 4',
      description: 'Integrating the backend APIs with the frontend.',
      status: 'pending'
    },
    {
      id: 4,
      title: 'Milestone 5',
      description: 'Running tests and deploying the project.',
      status: 'pending'
    }
  ];
  
  const statusClass = (status) => {
    switch (status) {
      case 'completed':
        return 'status-green';
      case 'pending':
        return 'status-white';
      case 'incomplete':
        return 'status-red';
      default:
        return '';
    }
  };
  </script>
  
  <style scoped>
  .container {
    background-color: #f3f4f6;
    padding: 24px;
  }
  
  .header {
    text-align: center;
    font-size: 1.5rem;
    padding-bottom: 48px;
    padding-top: 4rem;
    color: gray;
    font-weight: bold;
    margin-bottom: 1rem;
  }
  
  .content {
    max-width: 64rem;
    margin: 0 auto;
  }
  
  .grid {
    display: grid;
    grid-template-columns: 1fr;
    gap: 24px;
  }
  
  @media (min-width: 640px) {
    .grid {
      grid-template-columns: repeat(2, 1fr);
    }
  }
  
  .milestone-card {
    background-color: #fff;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    border-radius: 8px;
    transition: transform 0.2s ease-in-out;
    overflow: hidden;
  }
  
  .milestone-card:hover {
    transform: scale(1.05);
  }
  
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
  
  .status-green {
    background-color: #d1fae5;
    color: #047857;
  }
  
  .status-white {
    background-color: #ffffff;
    color: #374151;
    border: 1px solid #d1d5db;
  }
  
  .status-red {
    background-color: #fee2e2;
    color: #b91c1c;
  }
  
  .card-body {
    padding: 16px;
  }
  
  .card-body p {
    color: #4b5563;
    font-size: 1rem;
  }
  
  .completed {
    border-left: 8px solid #10b981;
  }
  
  .pending {
    border-left: 8px solid #f3f4f6;
  }
  
  .incomplete {
    border-left: 8px solid #ef4444;
  }
  </style>
  