<script setup lang="ts">
import { ref, onUnmounted } from 'vue'

// 🟢 親から受け取る設定値（Props）を定義
const props = defineProps<{
  title: string       // 音の名前
  frequency: number   // 周波数（Hz）
  intervalMs: number  // ON/OFFの切り替え周期（ms）
  audioCtx: AudioContext | null // 親から共通のAudioContextをもらう
}>()

const isPlaying = ref(false)

let intervalId: number | null = null
let oscillator: OscillatorNode | null = null
let gainNode: GainNode | null = null

const startAlert = async () => {
  if (isPlaying.value || !props.audioCtx) return

  if (props.audioCtx.state === 'suspended') {
    await props.audioCtx.resume().catch(() => {})
  }

  if (props.audioCtx.state === 'suspended') {
    console.warn("skip Audio")
    return
  }

  isPlaying.value = true

  // オシレーターとGainNodeの作成・接続
  oscillator = props.audioCtx.createOscillator()
  gainNode = props.audioCtx.createGain()

  oscillator.type = 'sine'
  oscillator.frequency.setValueAtTime(props.frequency, 0)
  
  oscillator.connect(gainNode)
  gainNode.connect(props.audioCtx.destination)
  oscillator.start(0)

  let soundOn = true

  // タイマーで音量を切り替える
  intervalId = window.setInterval(() => {
    if (!gainNode || !props.audioCtx) return
    const targetGain = soundOn ? 0.4 : 0
    gainNode.gain.setValueAtTime(targetGain, 0)
    soundOn = !soundOn
  }, props.intervalMs)
}

const stopAlert = () => {
  //if (!isPlaying.value) return

  if (intervalId) {
    clearInterval(intervalId)
    intervalId = null
  }

  if (oscillator) {
    try { oscillator.stop() } catch (e) {}
    oscillator.disconnect()
    oscillator = null
  }
  
  if (gainNode) {
    gainNode.disconnect()
    gainNode = null
  }

  isPlaying.value = false
}

const button = () => {
  if (isPlaying.value){
    stopAlert()
  }
  else{
    startAlert()
  }
}

// 🟢 このコンポーネント（画面からこの音が消えたら）自動でタイマーを消去
onUnmounted(() => {
  stopAlert()
})

defineExpose({
  startAlert,
  stopAlert
})
</script>

<template>
  <div class="flex flex-col items-center justify-center p-4 mx-15">
    <button @click="button" class="font-bold text-2xl">{{ props.title }}</button>
    <div :class="{ active: isPlaying }">
      {{ isPlaying ? "鳴動中" : "停止中" }}
    </div>
  </div>
</template>

