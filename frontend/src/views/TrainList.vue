<script setup lang="ts">
import { inject } from "vue"
import { RouterLink } from "vue"

const data = inject("wsData")
console.log(data)

</script>
<template>
  <p>{{data}}</p>
  <nav v-if="data">
    <p v-for="train in data.trains">
      id: {{train}}
    </p>
  </nav>
</template>
