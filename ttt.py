from datetime import datetime, timedelta
from telethon import TelegramClient, events
import pytz
from config import *


bot = TelegramClient('bot', API_ID, API_HASH).start(bot_token=TOKEN)
client = TelegramClient('session_ttt', API_ID, API_HASH)
client.start()
client.connect()


def update_vars():
    global names, names_letters, names_var, names_space, allnames_var, Maksym, Tanya, Yurii, YurikJr, Galya, Vitalii, m_space, t_space, y_space, yj_space, g_space, v_space, AllMaksym, AllTanya, AllYurii, AllYurikJr, AllGalya, AllVitalii, prevNum
    names = ["Maksym", "Tanya", "Yurii", "YurikJr", "Galya", "Vitalii"]
    names_letters = ['М', 'Т', 'С', 'Ю', 'Г', 'В']

    Maksym, Tanya, Yurii, YurikJr, Galya, Vitalii = 0, 0, 0, 0, 0, 0
    names_var = [Maksym, Tanya, Yurii, YurikJr, Galya, Vitalii]

    m_space, t_space, y_space, yj_space, g_space, v_space = ' ', ' ', ' ', ' ', ' ', ' '
    names_space = [m_space, t_space, y_space, yj_space, g_space, v_space]

    AllMaksym, AllTanya, AllYurii, AllYurikJr, AllGalya, AllVitalii = 0, 0, 0, 0, 0, 0
    allnames_var = [AllMaksym, AllTanya, AllYurii, AllYurikJr, AllGalya, AllVitalii]

    prevNum = 0


print('0')


def current_time():
    tz_kiev = pytz.timezone('Europe/Kiev')
    current_time = datetime.now(tz_kiev)

    timezone = int(current_time.utcoffset().total_seconds() / 3600) 
    return timezone 


async def startCount():
    update_vars()
    
    async def my_function(text):
        global names, names_letters, names_var, names_space, allnames_var, Maksym, Tanya, Yurii, YurikJr, Galya, Vitalii, m_space, t_space, y_space, yj_space, g_space, v_space, AllMaksym, AllTanya, AllYurii, AllYurikJr, AllGalya, AllVitalii, prevNum
 
        text.upper()
        num = int(text.split(" ")[0])
        id = text.split(" ")[1]
        for index, i in enumerate(names_letters):
            if id == i:
                names_var[index] += num - int(prevNum)
                prevNum = int(num)

    async def my_funct(text):
        global names, names_letters, names_var, names_space, allnames_var, Maksym, Tanya, Yurii, YurikJr, Galya, Vitalii, m_space, t_space, y_space, yj_space, g_space, v_space, AllMaksym, AllTanya, AllYurii, AllYurikJr, AllGalya, AllVitalii, prevNum
        text.upper()
        num = int(text.split(" ")[0])
        id = text.split(" ")[1]

        for index, i in enumerate(names_letters):
            if id == i:
                allnames_var[index] += num - int(prevNum)
                prevNum = int(num)

 
    global names, names_letters, names_var, names_space, allnames_var, Maksym, Tanya, Yurii, YurikJr, Galya, Vitalii, m_space, t_space, y_space, yj_space, g_space, v_space, AllMaksym, AllTanya, AllYurii, AllYurikJr, AllGalya, AllVitalii, prevNum
    messages = await client.get_messages(TTT_CHAT_USERNAME, limit=900, reverse=False)

    changable_time_delta = current_time()

    messages.reverse()
    abobus = True
    for message in messages:
        date = message.date + timedelta(hours=changable_time_delta)
        text = message.text.replace("*", "")
 
        if date.month == datetime.now().month and abobus == True:
            abobus = False
            prevNum = 0
 
        if (date.day == datetime.now().day and date.month == datetime.now().month):
            await my_function(text)
        elif date.month == datetime.now().month:
            await my_funct(text)
 
        else:
            prevNum = text.split(" ")[0]

@bot.on(events.NewMessage(pattern='/start'))
async def respond(event):
    global bot, names, names_letters, names_var, names_space, allnames_var, Maksym, Tanya, Yurii, YurikJr, Galya, Vitalii, m_space, t_space, y_space, yj_space, g_space, v_space, AllMaksym, AllTanya, AllYurii, AllYurikJr, AllGalya, AllVitalii, prevNum
    await startCount()
    
    curday = (datetime.now().day)
    month_max = 83
    dailyave = 3000
    n = 1000
    divisor = 3
    curnormal = curday * dailyave  # середнє на теперешній день

    maksymdiv, tanyadiv, yuriidiv, yuriijrdiv, galyadiv, vitaliidiv = 0, 0, 0, 0, 0, 0
    names_div = [maksymdiv, tanyadiv, yuriidiv, yuriijrdiv, galyadiv, vitaliidiv]
    for index_div, i_div in enumerate(names_div):
        names_div[index_div] = round(((allnames_var[index_div] + names_var[index_div]))/n/divisor)

    
    maksymvse, tanyavse, yuriivse, yuriijrvse, galyavse, vitaliivse = 0, 0, 0, 0, 0, 0
    names_vse = [maksymvse, tanyavse, yuriivse, yuriijrvse, galyavse, vitaliivse]
    for index_vse, i_vse in enumerate(names_vse):
        names_vse[index_vse] = allnames_var[index_vse]+names_var[index_vse]

        if names_vse[index_vse] == 0:
            names_space[index_vse] = '       '
        elif names_vse[index_vse] < 1000:
            names_space[index_vse] = '    '
        elif 1000 <= names_vse[index_vse] <= 10000:
            names_space[index_vse] = '   '
        elif 10000 < names_vse[index_vse] <= 100000:
            names_space[index_vse] = '  '
        else:
            names_space[index_vse] = ' '

        if names_vse[index_vse] >= 10000:
            names_vse[index_vse] = str(allnames_var[index_vse]+names_var[index_vse]).rjust(7)
        elif names_vse[index_vse] < 10000:
            names_vse[index_vse] = str(allnames_var[index_vse]+names_var[index_vse]).rjust(8)

    all_in_day = str(sum(names_var))

    spot_for_dots = 28
    sumbol = '.'

    maksymdots, tanyadots, yuriidots, yuriijrdots, galyadots, vitaliidots = 0, 0, 0, 0, 0, 0
    names_dots = [maksymdots, tanyadots, yuriidots, yuriijrdots, galyadots, vitaliidots]
    for index_dots, i_dots in enumerate(names_dots):
        names_dots[index_dots] = sumbol * names_div[index_dots] + (spot_for_dots - names_div[index_dots]) * ' '

        if names_div[index_dots] >= month_max/divisor:
            names_dots[index_dots] = sumbol * spot_for_dots

    response = ('M: 85000   Day: ' + str(all_in_day) + '   Now: ' + str(curnormal) + '\n\n')
    for i in range(6):
        line = names_vse[i] + names_space[i] + '[' + names_dots[i] + '] ' + ' ' + str(names_var[i]) + '  ' + names_letters[i] + '\n'
        response += line

    await event.respond(response)

def ttt_main():
    bot.run_until_disconnected()
    

if __name__ == '__main__':
    ttt_main()
