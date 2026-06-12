<script setup lang="ts">
import { inject, watch, ref, onUnmounted } from "vue"
import { RouterLink } from "vue-router"

const data = inject<any>("mqttData")

const trains = ref("--")
const topic = "test/pico"

watch(() => data?.value, (newData) => {
  newData.subscribe(topic)
  newData.on("message", function(topic, msg){
    console.log(msg)
    trains.value = msg.toString()
  })
  console.log(data)
})

console.log(data)

onUnmounted(() => {
  if(data?.value) {
    data.value.unsubscribe(topic)
    data.value.off("message")
  }
})

</script>
<template>
  <!-- <p>{{data}}</p> -->
  <h1>車両一覧</h1>
  <p>{{trains}}</p>
  <!-- <ul v-if="data"> -->
  <!--   <li v-for="train in data.trains">  -->
  <!--     <RouterLink :to="`train-list/${train.id}`"> -->
  <!--       id: {{train.id}}, 現在位置：{{train.read_id}} -->
  <!--     </RouterLink> -->
  <!--   </li> -->
  <!-- </ul> -->
</template>
