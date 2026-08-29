<script setup lang="ts">
import { Handle, Position } from "@vue-flow/core"
import type { MapNode } from "@/types/map.ts"

defineProps<{
  id: string
  data: {
    node: MapNode
  }
}>()
</script>
<template>
  <div class="block-node">
    <Handle
      type="target"
      :position="Position.Top"
    />

    <div class="block-name">
      {{ data.node.name }}
    </div>

    <div class="block-id">
      {{ data.node.id }}
    </div>

    <Handle
      type="source"
      :position="Position.Bottom"
    />
  </div>
</template>


