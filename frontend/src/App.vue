<template>
  <div id="app">
    <nav class="navbar">
      <h2>🎓 Student Performance Prediction</h2>

      <div class="menu">
        <router-link to="/">Dashboard</router-link>
      </div>
    </nav>

    <main class="content">
      <router-view />
    </main>
  </div>
</template>

<script setup lang="ts">
// No logic needed here (router handles everything)
</script>

<style>
body {
  margin: 0;
  font-family: Arial, Helvetica, sans-serif;
  background: #f4f6f9;
}

#app {
  min-height: 100vh;
}

/* NAVBAR */
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #1e293b; /* Upgraded to match your modern UI theme */
  color: white;
  padding: 15px 30px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

/* LINKS */
.menu a {
  color: #cbd5e1;
  text-decoration: none;
  margin-left: 20px;
  font-weight: 600;
  font-size: 0.95rem;
  padding-bottom: 4px;
}

.menu a.router-link-active {
  color: #38bdf8;
  border-bottom: 2px solid #38bdf8;
}

/* CONTENT AREA */
.content {
  padding: 0; /* Let Dashboard handle internal container padding */
}
</style>