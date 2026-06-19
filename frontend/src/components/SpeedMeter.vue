<script setup lang="ts">
  import { onMounted, ref, watch } from 'vue';
  import type { TRIReceivedTrainData } from '@/types/TRITypes';
  import speed_base from '@/assets/img/Meter/speed_base.png'
  import hari_img from "@/assets/img/Meter/hari.png"
  import atc_limPoint from '@/assets/img/Meter/atc_limPoint.png'
  import ATCNextLim from '@/assets/img/Meter/ATCNextLim.png'
  import mainLine from '@/assets/img/Meter/mainLine.png'
  import directionLine_OFF from '@/assets/img/Meter/directionLine_OFF.png'
  import forwardAlert_ON from '@/assets/img/Meter/forwardAlert_ON.png'
  import forwardAlert_OFF from '@/assets/img/Meter/forwardAlert_OFF.png'
  import Alert from "@/assets/sounds/Alert.mp3"
  import ATCSound from "@/assets/sounds/ATC-LimSpeedUpdate.WAV"

  let alertSound :HTMLAudioElement | null = null
  let ATCLimSpeedUpdate :HTMLAudioElement | null
  //let forwardAlert :HTMLAudioElement | null
  onMounted(()=>{
    ATCLimP_update(300);
    console.log("meter Mounted")
    alertSound = new Audio(Alert)
    ATCLimSpeedUpdate = new Audio(ATCSound)
    // ATCLimSpeedUpdate.volume = 1
    // forwardAlert = new Audio("sounds/forward-Alert.mp3")
  })
  const props = defineProps<{
    data : TRIReceivedTrainData ,
    clock : boolean  
  }>()

  const hari = ref<HTMLElement | null>(null)
  const ATC = ref<HTMLElement | null>(null)

  watch(()=>props.data , ( newValue , oldValue )=>{
    speed_update( oldValue.speed , newValue.speed)
    ATCLimP_update( newValue.lim )
  })

  watch(()=>props.data.lim , (newValue,oldValue)=>{
    if (props.data.atc){
      // ATCLimSpeedUpdate?.play()
    }
  })
  
  let isAni = false
  function speed_update( start:number , end:number ){
    if(!hari.value||isAni){return}
    isAni = true
    start=(start/1.5)-120
    end=(end/1.5)-120
    hari.value.animate(
    [ { transform: `rotate(${start}deg)` } , { transform: `rotate(${end}deg)` } ], 
    {
      fill: 'forwards', // 再生前後の状態（再生前、開始時の状態を適用）
      easing: 'linear',
      duration: 475, // 再生時間（1000ミリ秒）
    },).onfinish = ()=>{isAni = false}
  }
  
  function ATCLimP_update(lim:number){
    if(!ATC.value){return}
    lim=(lim/1.5)-120
    ATC.value.animate(
    [ { transform: `rotate(0deg)` } , { transform: `rotate(${lim}deg)` } ],
    {
      fill: 'forwards', // 再生前後の状態（再生前、開始時の状態を適用）
      duration: 0, // 再生時間（1000ミリ秒）
    },);
  }
  
  const trainAlert = ()=>{
    if (alertSound){
      alertSound.volume=1
      alertSound.play()
    }
  }
</script>
<template>
  <div style="position: relative; align-items: center;" @click="trainAlert" >
    <img :src="speed_base" style="width: 100%; margin: auto;" class="main" >
    <img :src="hari_img"  class="main" ref="hari" style="margin:auto">
    <img :src="atc_limPoint"  class="main" ref="ATC" v-show="data.atc" style="margin: auto;">
    <img :src="ATCNextLim" class="main" style="margin: auto;" ref="NextLim" v-show="props.data.forwardAlert && props.clock">
    <img :src="mainLine" class="sub" v-if="props.clock&&false">
    <img :src="directionLine_OFF" class="sub" v-else>
    <img :src="forwardAlert_ON" class="sub" style="top: 83%;" v-if="props.data.forwardAlert && props.clock">
    <img :src="forwardAlert_OFF" class="sub" style="top: 83%;" v-else>
  </div>
</template>
<style>
  .main{
    position: absolute;
    top: 0.2%;
    left: 0;
    right: 0;
    bottom: 0;
    width: 100%;
    transform-origin: 50% 50%;
    vertical-align: middle;
  }
  .sub{
    position: absolute;
    top: 75%;
    left: 50%;
    width: 35%;
    transform: translate(-50% , -50%);
  }
</style>
