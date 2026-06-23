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

interface TrainData{
  id: number,
  speed: number,
  limit: number,
  position: number,
  direction: number,
  mc: number
}

interface Trains{
  trains: TrainData[]
}

const trains = ref<any>(null)
const emergency = ref<EmergencyData | null>(null)
provide("trains", trains)
provide("emergency", emergency)

const handleMessage = (receivedTopic: string, msg: any) => {
  const rawData = msg.toString()
  console.log("生データ:",rawData)
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

let client: mqtt.MqttClient | null = null

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
    if (client) {
      client.subscribe(topics, (err) => {
        if(!err){
          console.log(`topics: ${topics.join(', ')}`)
        }
        else{
          console.error(err)
        }
      })
      client.off("message", handleMessage)
      client.on("message", handleMessage)
    }
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
