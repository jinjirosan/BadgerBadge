from flask import Flask, request
import paho.mqtt.client as mqtt
import json

app = Flask(__name__)

# MQTT Configuration
MQTT_BROKER = "172.16.234.55"  # Your MQTT broker IP
MQTT_PORT = 1883
MQTT_USER = "sigfoxwebhookhost"
MQTT_PASSWORD = "system1234"

# Decoding mappings
TARGET_CODES = {
    "t1": "wc",
    "t2": "living",
    "t3": "eva"
}

NAME_CODES = {
    "n1": "wc over",
    "n2": "douchen",
    "n3": "pootjes",
    "n4": "pyama",
    "n5": "aankleden"
}

def decode_message(target_code, name_code, duration):
    """Decode the compact message format into human-readable values"""
    target = TARGET_CODES.get(target_code, "unknown")
    name = NAME_CODES.get(name_code, "unknown")
    try:
        duration_secs = int(duration)
    except ValueError:
        duration_secs = 0
    return target, name, duration_secs

def publish_to_mqtt(topic, display_text, duration):
    try:
        client = mqtt.Client()
        client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        
        message = json.dumps({
            "name": display_text,
            "duration": int(duration)
        })
        
        client.publish(topic, message)
        client.disconnect()
        return True
    except Exception as e:
        print(f"Error publishing to MQTT: {e}")
        return False

@app.route('/sigfox', methods=['POST'])
def handle_webhook():
    try:
        # Get data from JSON body
        data = request.get_json()
        if not data:
            return 'Missing JSON body', 400

        target = data.get('target')
        name = data.get('name')
        duration = data.get('duration')

        if not all([target, name, duration]):
            return 'Missing required parameters', 400

        # Decode the message
        target, name, duration_secs = decode_message(target, name, duration)

        # Map display targets to MQTT topics
        topic_mapping = {
            'wc': 'home/displays/wc',
            'living': 'home/displays/living',
            'eva': 'home/displays/eva'
        }

        topic = topic_mapping.get(target.lower())
        if not topic:
            return f'Invalid target display: {target}', 400

        if publish_to_mqtt(topic, name, duration_secs):
            return 'OK', 200
        else:
            return 'Failed to publish to MQTT', 500

    except Exception as e:
        print(f"Error processing request: {e}")
        return str(e), 500

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000) 