<script setup lang="ts">
import { inject } from "vue"
const trains = inject<any>("trains")
</script>
<template>
  <div>
    <p>ここに運転台モニター</p>
    <!-- <p>{{data}}</p> -->
    <div>
      <div v-for="train in trains">
        <div v-if="train.id.toString() === $route.params.id">
          <p>{{train}}</p>
        </div>
      </div>
    </div>
  </div>
</template>
