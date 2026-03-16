<script setup lang="ts">
import { RouterLink } from "vue-router";
interface Links {
  label: string,
  path: string
}
const links: Links[] = [
  {label: "車載", path: "/train-list"},
  {label: "配線設定", path: "/settings"}
]

</script>
<template>
  <div class="w-full flex-col items-center m-8">
    <h1 class="font-bold text-5xl my-12">Welcome to TRI Control!</h1>
    <nav class="flex flex-wrap items-center gap-4">
      <RouterLink v-for="link in links" :to="link.path" class="flex items-center justify-center font-bold text-xl bg-blue-500 w-1/3 h-24 rounded-md text-white">
        {{link.label}}
      </RouterLink>
    </nav>
  </div>
</template>
