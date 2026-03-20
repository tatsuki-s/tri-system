<script setup lang="ts">
//import { defineProps } from 'vue'
const props = defineProps({
  trainData: String
})
</script>
<template>
  <p>ここに運転台モニター</p>
  <p>{{props.trainData}}</p>
</template>
