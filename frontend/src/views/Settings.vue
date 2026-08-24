<script setup lang="ts">
import { ref, inject } from "vue"

const map_list = inject<any>("map_list")
const map_now = inject<any>("map_now")
</script>
<template>
  <p>ここに閉塞設定画面</p>
  <p>現在：{{map_now}}</p>
  <p>map：{{map_list}}</p>
</template>
