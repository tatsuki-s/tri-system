<script setup lang="ts">
import { ref, inject, computed } from "vue"
import { useRoute } from "vue-router"
import SpeedMeter from "@/components/SpeedMeter.vue"
import { type TRIReceivedTrainData, TRIReceivedTrainDataDefault } from "@/types/TRITypes"
const trains = inject<any>("trains")
//const ReceivedData = ref<TRIReceivedTrainData>({...TRIReceivedTrainDataDefault})
const route = useRoute()
const ReceivedData = computed(() => {
  return trains.value.find(t => t.id.toString() === route.params.id)
})
const clock = ref(false)
//ReceivedData.value = 

</script>
<template>
  <div>
    <p>ここに運転台モニター</p>
    <div id="main" v-for="train in trains">
      <div v-if="train.id.toString() === $route.params.id"
        id="MainMonitor">
        <!-- <p>{{train}}</p> -->
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
