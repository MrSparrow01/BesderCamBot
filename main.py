import telebot.async_telebot
import socket
import json
import asyncio
from datetime import datetime
import pytz

BOT_TOKEN = "6439165432:AAG5L4nuWDadmgVtCInngYzOMBZNtwuYNd8"
CHAT_ID = "360805436"

bot = telebot.async_telebot.AsyncTeleBot(BOT_TOKEN)

async def write_to_file(text):
    with open('logs.txt', 'a') as file:
        file.write(text)

async def send_alarm_message(alarm_data):
    serial_number = alarm_data.get('SerialID')
    alert_event = alarm_data.get('Event')
    alert_time = alarm_data.get('StartTime')
    alert_status = alarm_data.get('Status')
    if serial_number == '44098fe28501926a':
        place = 'Door'
    elif serial_number == '81752845777b8188':
        place = "Garage"
    if alert_event == "HumanDetect":
        if alert_status == "Start":
            await bot.send_message(CHAT_ID,
                                   f"🚨 Warning! 🚨\nPlace: *{place}*\nEvent: Human Detection\nTime: {alert_time}",
                                   parse_mode='Markdown')
    else:
        with open('logs.txt', 'a') as file:
            file.write(f"[{alarm_data.get('StartTime')}] Place: {place} - Event: {alert_event}\n")

async def handle_client(reader, writer):
    addr = writer.get_extra_info('peername')
    kiev_time = pytz.timezone('Europe/Kiev').normalize(datetime.now(tz=pytz.utc)).strftime('%m-%d-%Y %H:%M:%S')
    await write_to_file(f"[{kiev_time}] Connection from {addr}\n")
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
            await write_to_file(f"[{kiev_time}] {e}\n")
    writer.close()
    await writer.wait_closed()

async def run_server(host='0.0.0.0', port=8080):
    server = await asyncio.start_server(handle_client, host, port)
    addr = server.sockets[0].getsockname()
    kiev_time = pytz.timezone('Europe/Kiev').normalize(datetime.now(tz=pytz.utc)).strftime('%m-%d-%Y %H:%M:%S')
    await write_to_file(f"[{kiev_time}] Serving on {addr}\n")
    async with server:
        await server.serve_forever()

@bot.message_handler(commands=['log'])
async def send_log(message):
    with open('logs.txt', 'rb') as file:
        await bot.send_document(CHAT_ID, file)

async def main():
    server_task = asyncio.create_task(run_server())
    bot_task = asyncio.create_task(bot.infinity_polling(skip_pending=True))
    await asyncio.gather(server_task, bot_task)

if __name__ == '__main__':
    asyncio.run(main())
