<script setup lang="ts">
import { inject } from "vue"
import { RouterLink } from "vue"

const data = inject("wsData")
console.log(data)
//if(data.type === "camera"){
  //console.log("this is camera")
//}

</script>
<template>
  <p>{{data}}</p>
</template>
