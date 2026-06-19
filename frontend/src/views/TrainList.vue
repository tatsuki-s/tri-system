<script setup lang="ts">
import { inject, watch, ref} from "vue"
import { RouterLink } from "vue-router"
import AudioBuzzer from "@/components/AudioBuzzer.vue"

const audioCtx = new (window.AudioContext || (window as any).webkitAudioContext)()
const emergencyButton = ref<InstanceType<typeof AudioBuzzer> | null>(null)

const trains = inject<any>("trains")

const emergency = inject<any>("emergency")
watch(emergency, (newData) => {
  if (newData){
    try{
      console.log(newData)
      if (newData.status === 1){
        emergencyButton.value?.startAlert()
      }
      else if (newData.status === 0){
        emergencyButton.value?.stopAlert()
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
