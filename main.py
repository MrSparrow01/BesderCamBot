import telebot
import socket
import json

BOT_TOKEN = "6439165432:AAG5L4nuWDadmgVtCInngYzOMBZNtwuYNd8"
CHAT_ID = "360805436"

bot = telebot.TeleBot(BOT_TOKEN)

def send_alarm_message(status, alarm_data):
    if status == "alarm":
        if alarm_data.get('Event') == "HumanDetect":
            if alarm_data.get('SerialID') == '44098fe28501926a':
                place = 'Door'
            elif alarm_data.get('SerialID') == '81752845777b8188':
                place = "Garage"
            if alarm_data.get('Status') == "Start":
                head = "🚨 Warning! 🚨"
            elif alarm_data.get('Status') == "Stop":
                head = "✅ All clear ✅"
            bot.send_message(CHAT_ID, f"{head}\nPlace: {place}\nEvent: {alarm_data.get('Event')}\nTime: {alarm_data.get('StartTime')}")
        else:
            pass
    elif status == "error":
        bot.send_message(CHAT_ID, f"Error:\n\n{str(alarm_data)}")
def run_server(host='0.0.0.0', port=8080):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host, port))
        s.listen()
        while True:
            conn, addr = s.accept()
            with conn:
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    try:
                        start_json = data.find(b'{')
                        if start_json != -1:
                            json_data = data[start_json:].decode('utf-8')
                            alarm_data = json.loads(json_data)
                            send_alarm_message("alarm", alarm_data)  # Send the message via Telegram
                    except json.JSONDecodeError as e:
                        send_alarm_message("error", e)
                    except Exception as e:
                        send_alarm_message("error", e)
                    finally:
                        conn.close()

if __name__ == '__main__':
    run_server()
