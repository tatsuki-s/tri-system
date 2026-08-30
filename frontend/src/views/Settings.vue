<script setup lang="ts">
import { inject, computed, type Ref } from "vue"
import type { Node, Edge } from '@vue-flow/core'  
import type { RailwayMap, MapNode } from "@/types/map.ts"
import { VueFlow } from '@vue-flow/core'
import '@vue-flow/core/dist/style.css'
import BlockNode from "@/components/BlockNode.vue"

const map_list = inject<RailwayMap[]>("map_list")
const map_now = inject<Ref<RailwayMap | null>>("map_now")
const mqttPublish = inject<any>("mqttPublish")

const nodeTypes = {
  block: BlockNode
}

const createFlowNodes = (map: RailwayMap): Node[] => {
  return map.nodes.map((node) => ({
    id: node.id,

    type: "block",

    position: node.position,

    data: {
      label: node.name,
      node
    }
  }))
}
const createFlowEdges = (map: RailwayMap): Edge[] => {
  const edges: Edge[] = []

  for (const route of map.routes) {
    const points = route.via ?? []

    const chain = [
      route.from,
      ...points,
      route.to
    ]

    for (let i = 0; i < chain.length - 1; i++) {
      edges.push({
        id: `${route.id}:${i}`,

        source: chain[i],
        target: chain[i + 1],

        type: 'default',

        data: {
          route
        }
      })
    }
  }

  return edges
}

const flowNodes = computed<Node[]>(() => {
  if (!map_now.value) return []

  return createFlowNodes(map_now.value)
})

const flowEdges = computed<Edge[]>(() => {
  if (!map_now.value) return []

  return createFlowEdges(map_now.value)
})

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
  <div id="flow_map">
    <VueFlow
      v-if="map_now"
      :nodes="flowNodes"
      :edges="flowEdges"
      :node-types="nodeTypes"
      fit-view-on-init
    />
  </div>
</template>
<style scoped>
#select_map{
  width: 100%;
  height: 10vh;
}
#flow_map{
  width: 100%;
  height: 95vh;
  border: 1px solid black;
}
.map_list_dropdown{
  height: 5vh;
}
</style>
