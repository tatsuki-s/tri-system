<script setup lang="ts">
import { inject, watch, ref, onUnmounted } from "vue"
import { RouterLink } from "vue-router"
import AudioBuzzer from "./asetts/AudioBuzzer.vue"

interface EmergencyData{
  status: number,
  sender: string
}

const audioCtx = ref<AudioContext | null >(null)
const emergencyButton = ref<InstanceType<typeof AudioBuzzer> | null>(null)

// ユーザーが最初に画面のどこかをクリックした時にAudioContextを初期化する（ブラウザ制限対策）
const initAudio = () => {
  if (!audioCtx.value) {
    audioCtx.value = new (window.AudioContext || (window as any).webkitAudioContext)()
  }
}
const data = inject<any>("mqttData")

const trains = ref("---")
const emergency = ref<EmergencyData | null>(null)
const topics = ["test/pico", "emergency"]

const handleMessage = (receivedTopic: string, msg: any) => {
  const rawData = msg.toString()
  console.log(rawData)
  switch(receivedTopic) {
    case "test/pico":
      trains.value = rawData
      break
    case "emergency":
      emergency.value = JSON.parse(rawData)
      if (emergency.value){
        if (emergency.value.status === 1){
          emergencyButton.value?.startAlert()
        }
        else if (emergency.value.status === 0){
          emergencyButton.value?.stopAlert()
        }
      }
      break
  }
}

watch(() => data?.value, (newData) => {
  if (newData) {
    newData.off("message", handleMessage)
    newData.subscribe(topics)
    newData.on("message", handleMessage)
  }
})

console.log(data)

onUnmounted(() => {
  if(data?.value) {
    data.value.unsubscribe(topics)
    data.value.off("message")
  }
})

</script>
<template>
  <div @click="initAudio()">
    <!-- <p>{{data}}</p> -->
    <h1>車両一覧</h1>
    <p>{{trains}}</p>
    <AudioBuzzer
        ref="emergencyButton"
        title="緊急"
        :frequency="2600"
        :interval-ms="100"
        :audio-ctx="audioCtx"
    />
    <!-- <p>{{emergency}}</p> -->
    <!-- <ul v-if="data"> -->
    <!--   <li v-for="train in data.trains">  -->
    <!--     <RouterLink :to="`train-list/${train.id}`"> -->
    <!--       id: {{train.id}}, 現在位置：{{train.read_id}} -->
    <!--     </RouterLink> -->
    <!--   </li> -->
    <!-- </ul> -->
  </div>
</template>
