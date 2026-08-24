<script setup lang="ts">
import { ref, inject } from "vue"
import type { Node, Edge } from '@vue-flow/core'  
import { VueFlow } from '@vue-flow/core'

//const select_map = ref<any>("")
const map_list = inject<any>("map_list")
const map_now = inject<any>("map_now")

</script>
<template>
  <p>現在：{{map_now}}</p>
  <p>map：{{map_list}}</p>
  <p>ここに閉塞設定画面</p>
  <select
    v-if="map_list"
    v-model=map_now
  >
    <option disabled value="">マップ変更時にテンプレートを選択</option>
    <option
        v-for="map_data in map_list"
        :key="map_data.description.id"
        :value="map_data"
    >
      {{map_data.description.name}}
    </option>
  </select>
  <p v-else>マップデータが読み込まれていません</p>
</template>
