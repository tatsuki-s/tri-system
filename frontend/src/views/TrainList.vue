<script setup lang="ts">
import { inject, watch, ref} from "vue"
import { RouterLink } from "vue-router"
import AudioBuzzer from "@/components/AudioBuzzer.vue"

const audioCtx = new (window.AudioContext || (window as any).webkitAudioContext)()
const emergencyButton = ref<InstanceType<typeof AudioBuzzer> | null>(null)

const trains = inject<any>("trains")
const emergency = inject<any>("emergency")
const mqttPublish = inject<any>("mqttPublish")
let isEmergency: Boolean = false
watch(emergency, (newData) => {
  if (newData){
    try{
      console.log(newData)
      if (newData.status === true){
        console.log("Ring!")
        isEmergency = true
        emergencyButton.value?.startAlert()
      }
      else if (newData.status === false){
        emergencyButton.value?.stopAlert()
        isEmergency = false
      }
    }
    catch{
      console.log("gomi")
    }
  }
},{deep: true, immediate: true})
</script>
<template>
  <div>
    <!-- <p>{{data}}</p> -->
    <h1>車両一覧</h1>
    <p>{{trains}}</p>
    <AudioBuzzer
        ref="emergencyButton"
        title="緊急"
        :frequency="2600"
        :interval-ms="100"
        :audio-ctx="audioCtx"
        @click='isEmergency = !isEmergency; mqttPublish("emergency", JSON.stringify({"status": isEmergency, "sender": "front"}), 0)'   
    />
    <p>{{emergency}}</p>
    <ul v-if="trains">
      <li v-for="train in trains"> 
        <!-- {{train}} -->
        <RouterLink :to="`train-list/${train.id}`">
          id: {{train.id}}, 現在位置：{{train.position}}
        </RouterLink>
      </li>
    </ul>
  </div>
</template>
