<template>
  <div class="ai-button"><RouterLink to="/chatInterface">Ai</RouterLink></div>
</template>

<style scoped>
.ai-button {
  position: fixed;
  bottom: 20px;
  right: 20px;
  width: 60px;
  height: 60px;
  background-color: #1f2937;
  color: white;
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 1rem;
  font-weight: bold;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  cursor: pointer;
  transition: transform 0.2s ease-in-out, background-color 0.2s ease-in-out;
}

.ai-button:hover {
  transform: scale(1.1);
}

.ai-button:active {
  transform: scale(1);
}
</style>
