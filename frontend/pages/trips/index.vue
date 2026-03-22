<template>
  <main>
    <h1>Trips</h1>
    <p>Browse available trips.</p>
    <ul>
      <li v-for="trip in trips" :key="trip.id">
        <NuxtLink :to="`/trips/${trip.id}`">{{ trip.name }}</NuxtLink>
      </li>
    </ul>
  </main>
</template>

<script setup lang="ts">
useHead({
  title: 'TravelHub - Trips',
})

const config = useRuntimeConfig()

const { data: trips } = await useFetch(`${config.public.apiBaseUrl}/trips`, {
  default: () => [],
})
</script>
