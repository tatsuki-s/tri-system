<script setup lang="ts">
import { inject, watch, ref} from "vue"
import { RouterLink } from "vue-router"
import EmergencyButton from "@/components/EmergencyButton.vue"


const trains = inject<any>("trains")
const emergency = inject<any>("emergency")
</script>
<template>
  <div>
    <!-- <p>{{data}}</p> -->
    <h1>車両一覧</h1>
    <p>{{trains}}</p>
    <EmergencyButton class="rounded-full size-50 bg-red-600 text-white font-bold"/>
    <p>{{emergency}}</p>
    <ul v-if="trains">
      <li v-for="train in trains"> 
        <!-- {{train}} -->
        <RouterLink :to="`train-list/${train.id}`">
          id: {{train.id}}, 現在位置：{{train.position}}
        </RouterLink>
      </li>
    </ul>
  </div>
</template>
