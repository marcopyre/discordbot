import os
import discord
from dotenv import load_dotenv
from datetime import datetime
from discord.ext import tasks
from selenium import webdriver

load_dotenv()
DISCORDTOKEN = os.getenv('DISCORD_TOKEN')
client = discord.Client()
now = datetime.now()


async def EDTprint(message):
    options = webdriver.ChromeOptions()
    options.headless = True
    driver = webdriver.Chrome(options=options)
    try:
        with open('EDTtarget.txt') as f:
            targetchannelid = f.readlines()
            channel = client.get_channel(int(targetchannelid[0]))
            EDT = True
    except:
        EDT = False

    if EDT == True:
        URL = 'https://edtmobiliteng.wigorservices.net//WebPsDyn.aspx?action=posEDTBEECOME&serverid=C&Tel=marco.pyre&date=' + str(
            now.month) + '/' + str(now.day) + '/' + str(
            now.year) + '&hashURL=182111c10833618378f0e0d2526928785ba0546e8b98e43cba9828ad74ef1e481ab0c7a40ac993520ed1317ee07811732ca421bdc03cea104a86f24b8e2f2f4f'
        driver.get(URL)
        S = lambda X: driver.execute_script('return document.body.parentNode.scroll' + X)
        driver.set_window_size(1280 , 720)
        driver.find_element_by_css_selector('#DivBody').screenshot('EDT.png')
        await channel.send(file=discord.File('EDT.png'))
        driver.quit()
    else:
        if message != False:
            await message.channel.send('EDT channel target is not defined use !setedtchannel to define it')


@tasks.loop(hours=1)
async def loop():
    print('up')
    if (now.hour == 12) and (datetime.today().weekday() == 6):
        await EDTprint(False)


@loop.before_loop
async def before():
    await client.wait_until_ready()


loop.start()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


@client.event
async def on_message(message):
    if message.content.lower() != '' and message.content.lower()[0] == '!':
        if message.content.lower() == '!edt':
            await EDTprint(message)
            await message.delete()
        if message.content.lower() == '!setedtchannel':
            with open('EDTtarget.txt', "w") as f:
                f.write(str(message.channel.id))
                await message.channel.send('EDT channel target set')


client.run(DISCORDTOKEN)
