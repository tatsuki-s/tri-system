<script setup lang="ts">
import { inject, ref, watch } from "vue"
import AudioBuzzer from "./AudioBuzzer.vue"

const emergency = inject<any>("emergency")
const mqttPublish = inject<any>("mqttPublish")

const audioCtx = new (
  window.AudioContext ||
  (window as any).webkitAudioContext
)()

const buzzer = ref<InstanceType<typeof AudioBuzzer> | null>(null)

const isEmergency = ref(false)

watch(
  emergency,
  (newData) => {
    if (!newData) return

    if (newData.status === true) {
      isEmergency.value = true
      buzzer.value?.startAlert()
    } else if (newData.status === false) {
      isEmergency.value = false
      buzzer.value?.stopAlert()
    }
  },
  {
    deep: true,
    immediate: true,
  }
)

const toggleEmergency = () => {
  const nextStatus = !isEmergency.value

  mqttPublish(
    "emergency",
    JSON.stringify({
      status: nextStatus,
      sender: "front",
    }),
    0
  )
}
</script>

<template>
  <AudioBuzzer
    ref="buzzer"
    title="緊急"
    :frequency="2600"
    :interval-ms="100"
    :audio-ctx="audioCtx"
    @click="toggleEmergency"
  />
</template>
