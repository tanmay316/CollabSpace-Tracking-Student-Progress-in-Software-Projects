<script setup>
import Milestone from '../components/Milestones.vue';
</script>

<template>
  <div class="milestone">
    <main>
      <Milestone/>
    </main>
  </div>
</template>

<style>
@media (min-width: 1024px) {
  .milestone {
    min-height: 100vh;
    display: flex;
    align-items: center;
  }
}
</style>