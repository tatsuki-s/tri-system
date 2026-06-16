<script setup lang="ts">
import { onMounted, onUnmounted, ref, provide } from 'vue'
import { RouterView } from 'vue-router'
import  mqtt from 'mqtt'

const mqttData = ref<any>(null)
const mqttUrl = import.meta.env.MQTT_HOST || "localhost"
const mqttPort = 9001

let client: mqtt.MqttClient | null = null

provide('mqttData', mqttData)

onMounted(() =>{
  const url = `ws://${mqttUrl}:${mqttPort}`
  client = mqtt.connect(url, {
    keepalive: 5, //5sec
    clientId: 'vue-' + Math.random().toString(16).substring(2, 8),
    clean: true,
    reconnectPeriod: 5000,
  })

  client.on('connect', () => {
    console.log("Connected")
    mqttData.value = client
  })

  client.on('close', () => {
    console.log("Disconnected")
  })

  client.on('error', (err: any) => {
    console.error('MQTT Connection Error:', err)
  })


})

onUnmounted(() => {
  if (client) {
    client.end()
  }
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
