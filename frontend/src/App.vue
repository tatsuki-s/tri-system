<script setup lang="ts">
import { onMounted, onUnmounted, ref, provide, watch } from 'vue'
import { RouterView } from 'vue-router'
import  mqtt from 'mqtt'

const mqttData = ref<any>(null)
const mqttUrl = import.meta.env.MQTT_HOST || "localhost"
const mqttPort = 9001

interface EmergencyData{
  status: number,
  sender: string
}

const trains = ref<any>(null)
const emergency = ref<EmergencyData | null>(null)
provide("trains", trains)
provide("emergency", emergency)

const handleMessage = (receivedTopic: string, msg: any) => {
  const rawData = msg.toString()
  console.log(rawData)
  switch(receivedTopic) {
    case "trains":
      trains.value = JSON.parse(rawData)
      break
    case "emergency":
      emergency.value = JSON.parse(rawData)
      break
  }
}

const topics = ["emergency", "trains"]
watch(() => mqttData?.value, (newData) => {
  if (newData) {
    newData.off("message", handleMessage)
    newData.subscribe(topics)
    newData.on("message", handleMessage)
  }
  },{immediate: true}
  )



let client: mqtt.MqttClient | null = null

//provide('mqttData', mqttData)

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
  if(mqttData?.value) {
    mqttData.value.unsubscribe(topics)
    mqttData.value.off("message", handleMessage)
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
