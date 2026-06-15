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

const startAlert = () => {
  if (isPlaying.value || !props.audioCtx) return

  isPlaying.value = true

  // オシレーターとGainNodeの作成・接続
  oscillator = props.audioCtx.createOscillator()
  gainNode = props.audioCtx.createGain()

  oscillator.type = 'sine'
  oscillator.frequency.setValueAtTime(props.frequency, props.audioCtx.currentTime)
  
  oscillator.connect(gainNode)
  gainNode.connect(props.audioCtx.destination)
  oscillator.start()

  let soundOn = true

  // タイマーで音量を切り替える
  intervalId = window.setInterval(() => {
    if (!gainNode || !props.audioCtx) return
    const targetGain = soundOn ? 0.2 : 0
    gainNode.gain.setValueAtTime(targetGain, props.audioCtx.currentTime)
    soundOn = !soundOn
  }, props.intervalMs)
}

const stopAlert = () => {
  if (!isPlaying.value) return

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
  <div class="buzzer-card">
    <h3>{{ title }}</h3>
    <p class="spec">({{ frequency }}Hz / 間隔: {{ intervalMs }}ms)</p>
    
    <button class="start-btn" @click="startAlert" :disabled="isPlaying">鳴らす</button>
    <button class="stop-btn" @click="stopAlert" :disabled="!isPlaying">止める</button>
    
    <span class="status-badge" :class="{ active: isPlaying }">
      {{ isPlaying ? "鳴動中" : "停止中" }}
    </span>
  </div>
</template>

<style scoped>
.buzzer-card {
  background: white;
  padding: 20px;
  margin: 15px 0;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
  text-align: left;
}
h3 { margin: 0 0 5px 0; font-size: 1.1rem; }
.spec { margin: 0 0 15px 0; color: #888; font-size: 0.85rem; }
button {
  font-weight: bold;
  padding: 8px 16px;
  margin-right: 10px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
button:disabled { opacity: 0.5; cursor: not-allowed; }
.start-btn { background-color: #ff4d4d; color: white; }
.stop-btn { background-color: #cccccc; color: #333; }
.status-badge {
  float: right;
  font-weight: bold;
  color: #999;
  margin-top: 8px;
}
.status-badge.active { color: #ff4d4d; }
</style>
