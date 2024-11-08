<script setup>
import MilestoneSubmissionFeedback from '../components/MilestoneSubmissionFeedback.vue';
</script>

<template>
  <div class="submission">
    <main>
      <MilestoneSubmissionFeedback/>
    </main>
  </div>
</template>

<style>
@media (min-width: 1024px) {
  .submission {
    min-height: 100vh;
    display: flex;
    align-items: center;
  }
}
</style>