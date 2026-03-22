<template>
  <div>
    <header>
      <nav>
        <NuxtLink to="/">Home</NuxtLink>
        <NuxtLink to="/trips">Trips</NuxtLink>
      </nav>
    </header>
    <slot />
    <footer>
      <p>&copy; {{ new Date().getFullYear() }} TravelHub</p>
    </footer>
  </div>
</template>
