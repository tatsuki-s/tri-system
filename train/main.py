import machine
import network
import uasyncio as asyncio
from umqtt.simple import MQTTClient

FORWARD_PIN = 6
REVERSE_PIN = 7
PWM_PIN = 2
DIR_PIN = 3
ADC_PIN = 26

MAX_DUTY = 65000

# 範囲を指定
VOLUME = [0, 1200, 2400, 5000, 6100, 8500, 11000, 13000, 15000, 17000, 19000, 60000]
# マスコンとしての値
# NOTCH = [4, 3, 2, 1, 0, -1, -2, -3, -4, -5, -6]
# ノッチに対する1mminあたりのdutyの増加量(stepになる)
MOTER_STEP = [400, 300, 200, 100, 0, -100, -200, -300, -400, -500, -1500]
WIFI_SSID = ""
WIFI_PASS = ""
MQTT_BROKER = ""
CLIENT_ID = "PicoW_Client0"
TOPIC = b"test/pico"

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(WIFI_SSID, WIFI_PASS)

adc = machine.ADC(ADC_PIN)
forward = machine.Pin(FORWARD_PIN,machine.Pin.IN,machine.Pin.PULL_UP)
reverse = machine.Pin(REVERSE_PIN,machine.Pin.IN,machine.Pin.PULL_UP)
# reverse = False
pwm = machine.PWM(machine.Pin(PWM_PIN))
pwm.freq(2000)
# Falseで正転，Trueで逆転
now_direc = False
direc = machine.Pin(DIR_PIN, machine.Pin.OUT)
prev_direc = None

duty = 0
step = 0

def generate_step(mc):
    for i in range(len(VOLUME)-1):
        if VOLUME[i] < mc < VOLUME[i+1]:
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

async def drive(limit_duty):
    # Falseで正転，Trueで逆転
    now_direc = False
    direc = machine.Pin(DIR_PIN, machine.Pin.OUT)
    # prev_direc = None

    duty = 0
    step = 0
    while True:
        mc_value = adc.read_u16()
        vol_step = generate_step(mc_value)
        switch_direc = get_direction()
        
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
            duty = limit_duty

        pwm.duty_u16(duty)
        
        print(generate_step(mc_value), now_direc, duty, mc_value)
        await asyncio.sleep(0.08)

async def mqtt_task():
    try:
        client = MQTTClient(CLIENT_ID, MQTT_BROKER)
        client.connect()
        
        while True:
            msg = "Hellllllo {}"
            client.publish(TOPIC, msg.encode())
            await asyncio.sleep(2)
    except Exeption as e:
        print(e)

    await asyncio.sleep(0.1)

async def main():
    while True:
        asyncio.gather(
            drive(MAX_DUTY),
            #,で追加
            mqtt_task()
        )

asyncio.run(main())
