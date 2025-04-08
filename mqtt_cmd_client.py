import paho.mqtt.client as mqtt
import subprocess

# MQTT Config
BROKER = "localhost"
TOPIC = "cmd/test"

def on_connect(client, userdata, flags, rc):
    print(f"[+] Connected to {BROKER} with result code {rc}")
    client.subscribe(TOPIC)

def on_message(client, userdata, msg):
    command = msg.payload.decode()
    print(f"[MQTT] Received command: {command}")
    try:
        result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, timeout=10)
        print(result.decode())
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Command failed:\n{e.output.decode()}")
    except Exception as ex:
        print(f"[ERROR] {str(ex)}")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, 1883, 60)
print(f"[MQTT] Listening for commands on topic '{TOPIC}'...")

client.loop_forever()
