<script setup lang="ts">
import { inject } from "vue"
const data = inject<any>("wsData")
</script>
<template>
  <p>ここに運転台モニター</p>
  <!-- <p>{{data}}</p> -->
  <div>
    <div v-for="train in data.trains">
      <div v-if="train.id.toString() === $route.params.id">
        <p>{{train}}</p>
      </div>
    </div>
  </div>
</template>
