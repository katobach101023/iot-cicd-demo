from flask import Flask
from flask_socketio import SocketIO
import paho.mqtt.client as mqtt
import json

APP_VERSION = "IoT API v2 – CI/CD enabled"

MQTT_BROKER = "broker.hivemq.com"
DATA_TOPIC = "iot/wokwi/data"
ACK_TOPIC = "iot/wokwi/ack"

app = Flask(__name__)
socketio = SocketIO(app)

@app.route("/")
def home():
    return APP_VERSION

def on_message(client, userdata, msg):
    payload = msg.payload.decode()
    try:
        data = json.loads(payload)
        print("Received:", data)

        # gửi ACK về ESP32
        ack = f"{APP_VERSION} – data received"
        client.publish(ACK_TOPIC, ack)

        socketio.emit("mqtt_data", data)

    except:
        print("Invalid JSON")

mqtt = mqtt.Client()
mqtt.connect(MQTT_BROKER, 1883)
mqtt.subscribe(DATA_TOPIC)
mqtt.on_message = on_message
mqtt.loop_start()

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)