<script setup lang="ts">
import { RouterLink } from "vue-router";
</script>
<template>
  <h1 class="font-bold text-5xl">Welcome to TRI Control!</h1>
  <nav>
    <RouterLink to="/train-list">車載</RouterLink>
    <br>
    <RouterLink to="/settings">閉塞設定</RouterLink>
  </nav>
</template>
