<script setup>
import Project from '../components/Project.vue';
</script>

<template>
  <div class="project">
    <main>
      <Project/>
    </main>
  </div>
</template>

<style>
@media (min-width: 1024px) {
  .project {
    min-height: 100vh;
    display: flex;
    align-items: center;
  }
}
</style>