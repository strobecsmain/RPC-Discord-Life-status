import time
import threading
import discord
from pypresence import Presence
import pystray
from PIL import Image, ImageDraw, ImageOps
from discord.ext import commands
import asyncio
import sys

# Конфигурация
client_id = 'CLIENT ID'
bot_token = 'TOKEN BOT'
guild_id = SERVER_ID
user_id = USER_ID

RPC = Presence(client_id)
RPC.connect()

start_time = int(time.time())
last_active_time = time.time()

activities = {
    "wake_up": {"state": "С этого моента", "details": "Я только проснулся", "large_image": "wake_up"},
    "eat": {"state": "С этого моента", "details": "Кушаю", "large_image": "eat"},
    "toilet": {"state": "С этого моента", "details": "В туалете", "large_image": "toilet"},
    "game": {"state": "С этого моента", "details": "Играю", "large_image": "game"},
    "busy": {"state": "С этого моента", "details": "Занят важными делами", "large_image": "busy"},
    "important_person": {"state": "С этого моента", "details": "Общаюсь с важным человеком",
                         "large_image": "important_person"},
    "away": {"state": "С этого моента", "details": "Отошел на некоторое время", "large_image": "away"},
    "nothing": {"state": "С этого моента", "details": "Ничего не делаю", "large_image": "nothing"},
}

current_activity = "wake_up"
invite_url = None
tray_icon = None  # Инициализация глобальной переменной для иконки трея


def update_activity():
    global current_activity, start_time, invite_url, tray_icon
    activity = activities[current_activity]
    elapsed_time = int(time.time()) - start_time if current_activity == "away" else None
    buttons = [{"label": "Присоединиться", "url": invite_url}] if invite_url and current_activity != "busy" else []

    activity_details = f"Что я сейчас делаю: **{activity['details']}**"
    if elapsed_time:
        activity_details += f"\nПрошло {elapsed_time // 60} минут"

    try:
        if buttons:
            RPC.update(
                state=activity["state"],
                details=activity_details,
                large_image=activity["large_image"],
                start=start_time,
                buttons=buttons
            )
        else:
            RPC.update(
                state=activity["state"],
                details=activity_details,
                large_image=activity["large_image"],
                start=start_time
            )
    except Exception as e:
        print(f"Ошибка обновления RPC: {e}")

    if tray_icon:
        tray_icon.title = activity["state"]  # Обновление заголовка иконки трея


def change_activity(activity, away_time=None):
    global current_activity, start_time, last_active_time
    current_activity = activity
    start_time = int(time.time())
    last_active_time = time.time()
    update_activity()

    if away_time:
        threading.Timer(away_time * 60, change_activity, args=("busy",)).start()


def monitor_inactivity():
    global last_active_time
    while True:
        if time.time() - last_active_time > 300:
            change_activity("away")
        time.sleep(60)


intents = discord.Intents.default()
intents.presences = True
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    await update_invite()


@bot.event
async def on_voice_state_update(member, before, after):
    if member.id == user_id:
        await update_invite()


async def update_invite():
    global invite_url
    guild = bot.get_guild(guild_id)
    member = guild.get_member(user_id)
    voice_state = member.voice

    if voice_state and voice_state.channel:
        channel = voice_state.channel
        invite = await channel.create_invite(max_age=300)
        invite_url = invite.url
    else:
        invite_url = None

    await update_activity_async()


async def update_activity_async():
    await bot.loop.run_in_executor(None, update_activity)


async def bot_start():
    await bot.start(bot_token)


async def shutdown():
    await bot.close()
    RPC.close()
    sys.exit()


def run_bot():
    asyncio.run(bot_start())


def tray_monitor():
    global tray_icon

    def create_image():
        try:
            image = Image.open("Frame-2.ico")  # замените на "icon.png" если у вас PNG
            return image
        except Exception as e:
            print(f"Ошибка загрузки иконки: {e}")
            width = 64
            height = 64
            color1 = "black"
            color2 = "white"
            image = Image.new("RGB", (width, height), color1)
            dc = ImageDraw.Draw(image)
            dc.rectangle((width // 2, 0, width, height // 2), fill=color2)
            dc.rectangle((0, height // 2, width // 2, height), fill=color2)
            return image

    def on_clicked(icon, item):
        activity_map = {
            "Ем": "eat",
            "В туалете": "toilet",
            "Играю": "game",
            "Занят": "busy",
            "Общаюсь с важным человеком": "important_person",
            "Ничего не делаю": "nothing"
        }

        if item.text in activity_map:
            change_activity(activity_map[item.text])
        elif item.text.startswith("Отошел"):
            away_time = int(item.text.split(" ")[1]) if len(item.text.split(" ")) > 1 else None
            change_activity("away", away_time)
        elif item.text == "Выход":
            icon.stop()
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(shutdown())

    tray_icon = pystray.Icon("SiresStatus", create_image(), activities[current_activity]["state"],
                             menu=pystray.Menu(
                                 pystray.MenuItem("Ем", on_clicked),
                                 pystray.MenuItem("В туалете", on_clicked),
                                 pystray.MenuItem("Играю", on_clicked),
                                 pystray.MenuItem("Занят", on_clicked),
                                 pystray.MenuItem("Общаюсь с важным человеком", on_clicked),
                                 pystray.MenuItem("Ничего не делаю", on_clicked),
                                 pystray.MenuItem("Отошел", pystray.Menu(
                                     pystray.MenuItem("5 минут", lambda: change_activity("away", 5)),
                                     pystray.MenuItem("10 минут", lambda: change_activity("away", 10)),
                                     pystray.MenuItem("30 минут", lambda: change_activity("away", 30)),
                                 )),
                                 pystray.MenuItem("Выход", on_clicked)
                             ))
    tray_icon.run()


# Запуск потоков
bot_thread = threading.Thread(target=run_bot, daemon=True)
bot_thread.start()

tray_thread = threading.Thread(target=tray_monitor, daemon=True)
tray_thread.start()

inactivity_thread = threading.Thread(target=monitor_inactivity, daemon=True)
inactivity_thread.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Выход из программы")
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(shutdown())
