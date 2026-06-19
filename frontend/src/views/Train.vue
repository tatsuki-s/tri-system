<script setup lang="ts">
import { ref, inject } from "vue"
import SpeedMeter from "@/components/SpeedMeter.vue"
import { type TRIReceivedTrainData, TRIReceivedTrainDataDefault } from "@/types/TRITypes"
const trains = inject<any>("trains")
const ReceivedData = ref<TRIReceivedTrainData>({...TRIReceivedTrainDataDefault})
const clock = ref(false)
</script>
<template>
  <div>
    <p>ここに運転台モニター</p>
    <div id="main" v-for="train in trains">
      <div v-if="train.id.toString() === $route.params.id"
        id="MainMonitor">
        <p>{{train}}</p>
        <SpeedMeter
          id="SpeedMeter"
          :data="ReceivedData", 
          :clock="clock"/>
      </div>
    </div>
  </div>
</template>
<style scoped>
#main{
  display: flex; 
  align-items: center;
}
#MainMonitor{
  height: 100vh;
  width: 100vw;
}
#SpeedMeter{
  width: 40vw; 
  height: 40vw;
  margin: 2vw;
}
</style>
