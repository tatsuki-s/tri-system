<script setup lang="ts">
import { inject, type Ref } from "vue"
import type { RailwayMap } from "@/types/map.ts"
import '@vue-flow/core/dist/style.css'

const map_list = inject<RailwayMap[]>("map_list")
const map_now = inject<Ref<RailwayMap | null>>("map_now")
const mqttPublish = inject<any>("mqttPublish")

const selectMapTemplate = () => {
  mqttPublish("map/now", JSON.stringify(map_now.value), 1, true)
  console.log("map_now", JSON.stringify(map_now.value))
}

</script>
<template>
  <!-- <p>現在：{{map_now}}</p> -->
  <!-- <p>map：{{map_list}}</p> -->
  <div id="select_map">
    <p>ここに閉塞設定画面</p>
    <select
      v-if="map_list"
      v-model="map_now"
      @change="selectMapTemplate"
    >
      <option
        disabled
        value=null
        class="map_list_dropdown"
      >
        マップ変更時にテンプレートを選択</option>
      <option
        class="map_list_dropdown"
        v-for="map_data in map_list"
        :key="map_data.description.id"
        :value="map_data"
      >
        {{map_data.description.name}}
      </option>
    </select>
    <p v-else>マップデータが読み込まれていません</p>
  </div>
  <div v-if="map_now" id="main_line" class="w-1/2">
    <!-- <p>{{map_now["map"] || "map not selected"}}</p> -->
    <ul>
      <li v-for="marker in map_now['map']" class="flex items-center m-4">
        <!-- {{marker}} -->
        <div class="flex flex-col border-1 w-50 p-4">
          <div>{{ marker.id }}番 {{marker.name}}</div>
          <div>↑
            <!-- <input>{{marker.limit.back}}</input> -->
            <select 
              v-model="marker.limit.back" 
              @change="selectMapTemplate"
              class="border rounded p-1 w-30"
            >
              <option :value="0">停止 (0)</option>
              <option :value="80">警戒 (80)</option>
              <option :value="160">注意 (160)</option>
              <option :value="240">減速 (240)</option>
              <option :value="300">進行 (300)</option>
            </select> 
          </div>
          <div>↓
            <!-- <input>{{marker.limit.front}}</input> -->
            <select 
              v-model="marker.limit.front" 
              @change="selectMapTemplate"
              class="border rounded p-1 w-30"
            >
              <option :value="0">停止 (0)</option>
              <option :value="80">警戒 (80)</option>
              <option :value="160">注意 (160)</option>
              <option :value="240">減速 (240)</option>
              <option :value="300">進行 (300)</option>
            </select> 
          </div>

        </div>
        <div class="w-2/10 m-4">
          <div v-if="marker.train">{{marker.train}}</div>
          <div v-else>車両なし</div>
        </div>

      </li>
    </ul>
  </div>
</template>
<style scoped>
#select_map{
  width: 100%;
  height: 10vh;
}
.map_list_dropdown{
  height: 5vh;
}
</style>
