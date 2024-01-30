import telebot.async_telebot
import socket
import json
import asyncio
from datetime import datetime
import pytz
import re

BOT_TOKEN = "6439165432:AAG5L4nuWDadmgVtCInngYzOMBZNtwuYNd8"
CHAT_ID = "360805436"

bot = telebot.async_telebot.AsyncTeleBot(BOT_TOKEN)

reference_minute = ""
alert = True

class IsAdmin(telebot.asyncio_filters.SimpleCustomFilter):
    key='is_me'
    @staticmethod
    async def check(message: telebot.types.Message):
        if message.from_user.id == 360805436: return True
        else: return False

async def write_to_file(text):
    kiev_time = pytz.timezone('Europe/Kiev').normalize(datetime.now(tz=pytz.utc)).strftime('%Y-%m-%d %H:%M:%S')
    with open('logs.txt', 'a') as file:
        file.write(f"[{kiev_time}] {text}\n")

async def send_alarm_message(alarm_data):
    global reference_minute
    serial_number = alarm_data.get('SerialID')
    alert_event = alarm_data.get('Event')
    alert_time = alarm_data.get('StartTime')
    alert_status = alarm_data.get('Status')
    current_minute = re.search(r'(\d+):(\d+):(\d+)', alert_time)[2]
    if serial_number == '44098fe28501926a':
        place = 'Door'
    elif serial_number == '81752845777b8188':
        place = "Garage"
    if alert_event == "HumanDetect":
        if alert_status == "Start" and alert:
            if current_minute != reference_minute:
                await bot.send_message(CHAT_ID,
                                   f"🚨 Warning! 🚨\nPlace: *{place}*\nEvent: Human Detection\nTime: {alert_time}",
                                   parse_mode='Markdown')
                reference_minute = current_minute
            else:
                await write_to_file(f"Place: {place} - Event: Human Detection")
    else:
        await write_to_file(f"Place: {place} - Event: {alert_event}")

async def handle_client(reader, writer):
    addr = writer.get_extra_info('peername')
    await write_to_file(f"Connection from {addr}")
    while True:
        data = await reader.read(1024)
        if not data:
            break
        try:
            start_json = data.find(b'{')
            if start_json != -1:
                json_data = data[start_json:].decode('utf-8')
                alarm_data = json.loads(json_data)
                await send_alarm_message(alarm_data)
        except Exception as e:
            await write_to_file(e)
    writer.close()
    await writer.wait_closed()

async def run_server(host='0.0.0.0', port=8080):
    server = await asyncio.start_server(handle_client, host, port)
    addr = server.sockets[0].getsockname()
    await write_to_file(f"Serving on {addr}")
    async with server:
        await server.serve_forever()


@bot.message_handler(commands=['start'])
async def start_command(message):
    await write_to_file(f"Somebody have started bot.\nUsername: {message.from_user.username}\n"
                        f"Name: {message.from_user.first_name}\nID: {message.from_user.id}\n")

@bot.message_handler(commands=['log'], is_me=True)
async def send_log():
    with open('logs.txt', 'rb') as file:
        await bot.send_document(CHAT_ID, file)

@bot.message_handler(commands=['alert_on'], is_me=True)
async def turn_on_alert():
    global alert
    alert = True
    await bot.send_message(CHAT_ID, "Notification is *ON*", parse_mode="Markdown")

@bot.message_handler(commands=['alert_off'], is_me=True)
async def turn_off_alert():
    global alert
    alert = False
    await bot.send_message(CHAT_ID, "Notification is *OFF*", parse_mode="Markdown")

async def main():
    server_task = asyncio.create_task(run_server())
    bot_task = asyncio.create_task(bot.infinity_polling(skip_pending=True))
    await asyncio.gather(server_task, bot_task)

if __name__ == '__main__':
    asyncio.run(main())
