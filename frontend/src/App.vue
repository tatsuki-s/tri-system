<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { RouterLink, RouterView } from 'vue-router'

let socket = null
const wsData = ref("")
onMounted(() =>{
  socket = new WebSocket("ws://localhost:8000/ws")

  socket.onmessage = (msg) => {
    console.log("message:", msg.data)
    wsData.value = msg.data
  }
})
</script>

<template>
  <header>
    <div>

      <p>{{wsData}}</p>

      <nav>
        <RouterLink to="/">Home</RouterLink>
        <RouterLink to="/about">About</RouterLink>
      </nav>
    </div>
  </header>

</template>

<style scoped>
</style>
