<script setup lang="ts">
import { onMounted, ref, provide } from 'vue'
import { RouterView } from 'vue-router'

let socket = null
const wsData = ref(null)
const wsUrl = import.meta.env.WS_HOST || "localhost"
onMounted(() =>{
  socket = new WebSocket(`ws://${wsUrl}:8000`)

  socket.onmessage = (msg) => {
    console.log("message:", msg.data)
    wsData.value = JSON.parse(msg.data)
  }

  provide("wsData", wsData)
})
</script>
<template>
  <header>
    <div>
      <RouterView />
    </div>
  </header>
</template>

<style scoped>
</style>
