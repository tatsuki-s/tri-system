<script setup lang="ts">
import { inject } from "vue"
import { RouterLink } from "vue-router"

const data = inject<any>("wsData")

console.log(data)

</script>
<template>
  <!-- <p>{{data}}</p> -->
  <h1>車両一覧</h1>
  <ul v-if="data">
    <li v-for="train in data.trains"> 
      <RouterLink :to="`train-list/${train.id}`">
        id: {{train.id}}, 現在位置：{{train.read_id}}
      </RouterLink>
    </li>
  </ul>
</template>
