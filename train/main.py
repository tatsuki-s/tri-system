import machine
import json
import gc
import network
import uasyncio as asyncio
from mqtt_as import MQTTClient, config as mconf
import config

FORWARD_PIN = 6
REVERSE_PIN = 7
PWM_PIN = 3
DIR_PIN = 2
ADC_PIN = 26
EMERGENCY_PIN = 8

MAX_DUTY = 65000

WIFI_SSID = config.WIFI_SSID
WIFI_PASS = config.WIFI_PASS
# MQTT_BROKER = config.MQTT_BROKER

VOLUME = config.VOLUME
MOTER_STEP = config.MOTER_STEP

CLIENT_ID = config.CLIENT_ID
PUB_TOPIC = f"train/{CLIENT_ID}"
READ_TOPIC = f"train/{CLIENT_ID}/limit"


uart = machine.UART(0, baudrate=9600, tx=machine.Pin(0), rx=machine.Pin(1), timeout=10)

# wlan = network.WLAN(network.STA_IF)
# wlan.active(True)
# wlan.connect(config.WIFI_SSID, config.WIFI_PASS)
    
mconf["ssid"] = config.WIFI_SSID
mconf["wifi_pw"] = config.WIFI_PASS
mconf["server"] = config.MQTT_BROKER
mconf["client_id"] = CLIENT_ID
mconf["keepalive"] = 60
mconf["queue_len"] = 1 

client = MQTTClient(mconf)
client.DEBUG = True
is_connected = False
is_emergency = False

mqtt_data = {
    "id": CLIENT_ID,
    "speed": 0,
    # "limit": 0,
    "position": 0, # UART経由で今後実装
    "direction": True,
    "mc": 0
    }
limit = 0

async def drive():
    global mqtt_data, is_emergency, limit
    adc = machine.ADC(ADC_PIN)
    forward = machine.Pin(FORWARD_PIN,machine.Pin.IN,machine.Pin.PULL_UP)
    reverse = machine.Pin(REVERSE_PIN,machine.Pin.IN,machine.Pin.PULL_UP)
    pwm = machine.PWM(machine.Pin(PWM_PIN))
    pwm.freq(2000)
    # Falseで正転，Trueで逆転
    now_direc = False
    direc = machine.Pin(DIR_PIN, machine.Pin.OUT)
    # prev_direc = None
    emergency = machine.Pin(EMERGENCY_PIN,machine.Pin.IN,machine.Pin.PULL_UP)

    duty = 0
    step = 0

    def generate_step(mc):
        for i in range(len(VOLUME)-1):
            low = min(VOLUME[i], VOLUME[i+1])
            high = max(VOLUME[i], VOLUME[i+1])
            if low <= mc < high:
                return MOTER_STEP[i]
        return 0

    def get_direction():
        if reverse.value() == 0 and forward.value() == 1:
            return False
        elif reverse.value() == 1 and forward.value() == 0:
            return True
        else:
            return None

    now_direc = get_direction()

    while True:
        mc_value = adc.read_u16()
        vol_step = generate_step(mc_value)
        switch_direc = get_direction()
        limit_duty = min(limit * 200, MAX_DUTY)

        if emergency.value() == 0:
            is_emergency = True
            print("EMERGENCY!")
        
        print(duty, limit)
        if (switch_direc != now_direc) or (switch_direc is None):
            if duty > 0:
                step = -2000
            else:
                step = 0
                if switch_direc is not None:
                    now_direc = switch_direc
        else:
            step = vol_step
            
        duty += step

        if now_direc is False:
            direc.on()
        else:
            direc.off()
                
        if duty < 0:
            duty = 0
        if duty > limit_duty:
            duty -= 2000
            if duty < limit_duty:
                duty = limit_duty

        pwm.duty_u16(duty)
        
        # print(generate_step(mc_value), now_direc, duty, mc_value)
        mqtt_data["speed"] = duty // 200
        mqtt_data["direction"] = now_direc 
        mqtt_data["mc"] = generate_step(mc_value)
        await asyncio.sleep(0.08)

#受信処理
async def mqtt_read():
    global limit
    async for topic, msg, retained in client.queue:
        try:
            data = json.loads(msg)
            print("受信:", topic, data)
            limit = int(data)
        except Exception as e:
            print("受信処理エラー:", e)

#送信処理
async def mqtt_send():
    global mqtt_data, is_connected, is_emergency
    is_connected = False
    # await client.connect()
    led = machine.Pin("LED", machine.Pin.OUT)
    emergency_data = {"status": True, "sender": f"train{mqtt_data["id"]}" }

    while True:
        # print(wlan.isconnected(), is_connected, gc.mem_free(), wlan.status())
        if client._has_connected:
            led.on()
            #mqttの再接続
            try:
                await client.publish(PUB_TOPIC, json.dumps(mqtt_data).encode()) #[]で囲っているのは暫定
                if is_emergency:
                    await client.publish("emergency", json.dumps(emergency_data).encode()) 
                    is_emergency = False
                # await asyncio.sleep(5)
            except Exception as e:
                print("送信エラー", e)
                is_connected = False
        else:
            led.off()
        print(limit)
        await asyncio.sleep(1.0)

async def receive_uart():
    global mqtt_data, uart
    while True:
        if uart.any():
            try:
                data = uart.readline().decode("utf-8").strip()
                mqtt_data["position"] = int(data)
            except Exception as e:
                print(e)
        await asyncio.sleep(0.3)

async def mqtt_subscribe_on_reconnect():
    while True:
        await client.up.wait()
        client.up.clear()
        print("mqtt接続確立。subscribeします。")
        await client.subscribe(READ_TOPIC, 0)

async def main():
    try:
        await client.connect(quick=True)
    except Exception as e:
        print(e)
    await asyncio.gather(

        drive(),
        #,で追加
        mqtt_send(),
        mqtt_read(),
        mqtt_subscribe_on_reconnect(),
        receive_uart()
    )

asyncio.run(main())
