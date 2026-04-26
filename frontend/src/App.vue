<script setup lang="ts">
import { onMounted, onUnmounted, ref, provide } from 'vue'
import { RouterView } from 'vue-router'
import  mqtt from 'mqtt'

const mqttData = ref(null)
const mqttUrl = import.meta.env.MQTT_HOST || "localhost"
const mqttPort = 9001

let client: mqtt.MqttClient | null = null

onMounted(() =>{
  const url = `mqtt://${mqttUrl}:${mqttPort}`
  client = mqtt.connect(url, {
    keepalive: 60,
    clientId: 'vue-' + Math.random().toString(16).substring(2, 8),
  })

  client.on('connect', () => {
    console.log("Connected")
    client?.subscribe('test/pico', (err: any) => {
      if(!err){
        console.log('subscribed')
      }
    })
  })

  client.on('message', (topic: any, message: any) => {
    // messageはBufferなので文字列に変換してパース
    console.log(`Topic: ${topic}, Message: ${message.toString()}`)
    try {
      mqttData.value = JSON.parse(message.toString())
    } catch (e) {
      mqttData.value = message.toString()
    }
  })

  client.on('error', (err: any) => {
    console.error('MQTT Connection Error:', err)
  })

  provide('mqttData', mqttData)

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
