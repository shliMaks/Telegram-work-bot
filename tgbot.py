from telethon.sync import TelegramClient, events
from telethon.tl.types import *
import pyautogui
import time
import re
import random
import pygame
from config import *
from GUI_keys import *



pygame.mixer.init()
try:
    sound = pygame.mixer.Sound("boop.wav")
    sound_file_exist = True
except Exception as e:
    sound_file_exist = False


client = TelegramClient('tgbot_name', API_ID, API_HASH)
client.connect()

if not client.is_user_authorized():
    client.send_code_request(PHONE_NUMBER)
    client.sign_in(PHONE_NUMBER, input('Enter the code: '))

url_pattern = r'https?://\S+'
key_cords = {
             "a": [(80, 925)],
             "s": [(220, 925)],
             "d": [(360, 925)],
             "e": [(100, 500)],
            }
yes_links = [
             "mdisk.",
             "disk.",
             "mega.nz",
             "dood.pm",
             "xdisc.in",
             "pornhub.com",
             "xnxx.com",
             "xlxx.com",
             "xvedos.com",
             "xvideos.com",
             "s.id",
             ]
maybe_links = [
               "t.me",
               "@",
              ]
no_links = [
            "amzn.",
            "ojueg.es",
            "#",
            "rbc.ua",
            '/'
           ]
skip_phrases = [

                "child_abuse",
                "Does this contain sex or nudity?",
                "Please return to previous report",
                "stats",
                "Comments",
                ]


def click_on_cords(key):
    if key in key_cords:
        cords = key_cords[key]
        for cord in cords:
            pyautogui.click(cord)
            time.sleep(0.1)

def check_links(message, if_no_text):
    if message.text: 
        # перевірка на вписані силки
        for link in yes_links:
            if link in message.text:
                return "d"
        for link in maybe_links:
            if link in message.text:
                return "s"
        # перевірка на навписані силки
        if message.raw_text:
            matches = re.findall(url_pattern, message.raw_text)
            if matches:
                return "s"
        if message.entities:
            for entity in message.entities:
                condition = isinstance(entity, (MessageEntityUrl, MessageEntityTextUrl, MessageEntityMention, MessageEntityMentionName))
                if condition:
                    return "s"
                condition_two = isinstance(entity, (MessageEntityCustomEmoji))
                if condition_two:
                    if "🍆" in message.raw_text:
                        return "s"
                    return "a"
        for link in no_links:
            if link in message.text:
                return "a"
        if not message.entities:
            return "a"

        return "a"
    else: # якщо немає тексту 
        return if_no_text   

def message_type_check(message):
    if message.media:
        if isinstance(message.media, MessageMediaDocument):
            # стікери
            if any(isinstance(attr, DocumentAttributeSticker) for attr in message.media.document.attributes):
                pass
            # відео
            elif any(isinstance(attr, DocumentAttributeVideo) for attr in message.media.document.attributes):
                if hasattr(message.media, 'spoiler') and message.media.spoiler:
                    return "e"
                pass
            # музика голосові
            elif any(isinstance(attr, DocumentAttributeAudio) for attr in message.media.document.attributes):
                return check_links(message, "a")
            # файли  
            else:
                return "d"
        # фото
        elif isinstance(message.media, MessageMediaPhoto):
            if hasattr(message.media, 'spoiler') and message.media.spoiler:
                return "e"
            pass  
        #  голосування
        elif isinstance(message.media, MessageMediaPoll):
            return check_links(message, "a")
        # веб сторінки
        elif hasattr(message.media, 'webpage') and isinstance(message.media.webpage, WebPage):
            pass
    # текст
    elif message.media is None:
        return check_links(message, "a")


# ------------------------------------------------------------------------

result = None


@client.on(events.NewMessage)
async def handle_incoming_message(event):
    global result
    sender = await event.get_sender()
    message_text = event.raw_text

    if sender.username == CHAT_USERNAME:
        if not "Does this contain sex or nudity?" in message_text:
            result = message_type_check(event)

        if "Does this contain sex or nudity?" in message_text:
            if event.message.buttons and result:
                if result == "e":
                    click_on_cords(result)
                
                if sound_file_exist:
                    sound.play()

                rand_time = random.randint(260, 380) / 1000
                time.sleep(rand_time)

                if result == "a":  # Перша кнопка
                    await event.message.click(0, 0)
                elif result == "s":  # Друга кнопка
                    await event.message.click(0, 1)
                elif result == "d":  # Третя кнопка
                    await event.message.click(0, 2)

                if sound_file_exist:
                    sound.stop()




async def main():
    await client.start(phone=PHONE_NUMBER)
    print("Client is running")
    await client.run_until_disconnected()


def start_auto_worker():
    try:
        client.loop.run_until_complete(main())
    except KeyboardInterrupt:
        client.disconnect()
        print("Client disconnected")


if __name__ == "__main__":
    start_auto_worker()


