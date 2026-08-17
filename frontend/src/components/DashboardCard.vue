<template>
  <div class="card">
    <h3>{{ title }}</h3>
    <h1>{{ value }}</h1>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  title: string
  value: string | number
}>()
</script>

<style scoped>
.card{
    background:white;
    border-radius:10px;
    padding:20px;
    box-shadow:0 2px 8px rgba(0,0,0,.1);
    text-align:center;
}

h1{
    color:#42b883;
    margin-top:10px;
}
</style>