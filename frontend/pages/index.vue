<template>
  <main>
    <section class="hero">
      <h1>Welcome to TravelHub</h1>
      <p>Plan your next adventure with ease.</p>
      <NuxtLink to="/trips">Explore Trips</NuxtLink>
    </section>
  </main>
</template>

<script setup lang="ts">
useHead({
  title: 'TravelHub - Home',
})
</script>
