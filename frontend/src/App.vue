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
      <nav>
        <RouterLink to="/train-list" :props="wsData">車載</RouterLink>
        <br>
        <RouterLink to="/settings">閉塞設定</RouterLink>
      </nav>
      <RouterView />
    </div>
  </header>

</template>

<style scoped>
</style>
