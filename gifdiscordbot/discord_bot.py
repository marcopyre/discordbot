import os
import discord
import urllib.request
import json
import random
from dotenv import load_dotenv
from os import listdir
from os.path import isfile, join
from datetime import datetime
from discord.ext import tasks

messages = []
ranarray = []
gifs = []
file = 0;
target = False

def timedmessages():
    now = datetime.now()
    data = ''
    condition = ''
    timedmsgs = open('timed_messages.txt', 'r')
    timedLines = timedmsgs.readlines()
    for line in timedLines:
        heures = []
        for row in line.split('|')[0].split(','):
            heures.append(row.replace('heure: ', ''))
        minutes = []
        for row in line.split('|')[1].split(','):
            minutes.append(row.replace('minute: ', ''))
        message = line.split('|')[2].replace('-HEURE-', ' ' + str(now.hour) + 'h').replace('message:', '')
        if str(now.hour) in heures and str(now.minute) in minutes and now.second == 0:
            data = message
    return data

# fonction transformant les fichier stockant les gif en tableau
def reader(filename):
    exec(filename + "links = open('giflinks/'+ filename +'.txt', 'r', encoding='utf-8')")
    exec(filename + "lines = " + filename + "links.readlines()")
    outputarray = []
    exec(
        "row = 0\n"
        "ranarray.append(False)\n"
        "for line in " + filename + "lines:\n"
                                    "   row +=1\n"
                                    "   if row == 2:\n"
                                    "       x = line.strip()\n"

                                    "   if row >= 4:\n"
                                    "       outputarray.append(line.strip())\n"
                                    "   if row > 4:\n"
                                    "       ranarray[file] = True\n"
                                    "messages.append(x.split())\n"
                                    "file += 1\n"
                                    "gifs.append(outputarray)"
    )
    return outputarray


# fonction condition d'affichage des gifs
async def gifprint(sender, message, wordsarray, gif, number, multigif):
    if multigif != False:
        if message in wordsarray:
            ran = random.randint(0, len(gif) - 1)
            await sender.channel.send(gif[ran])
    else:
        if message in wordsarray:
            await sender.channel.send(gif[int(number)])


files = [f for f in listdir("giflinks") if isfile(join("giflinks", f))]
for i in range(len(files)):
    exec(files[i].replace('.txt', '') + "array = reader('" + files[i].replace('.txt', '') + "')")

checker = []

for i in range(len(messages)):
    for j in range(len(messages[i])):
        checker.append(messages[i][j])

load_dotenv()
DISCORDTOKEN = os.getenv('DISCORD_TOKEN')
GIPHYTOKEN = 'dc6zaTOxFJmzC' #token web publique
client = discord.Client()

if os.path.isfile('targetchannel.txt') == True:
    with open('targetchannel.txt') as f:
        targetchannelid = f.readlines()
        target = True
else:
    targetchannel = os.getenv('GENERAL_CHANNEL_ID')

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


@client.event
async def on_message(message):
    print(message.content.lower())

    if message.content.lower()[0] == '!' and message.content.lower() is not None:
        if message.content.lower() == '!EDT':
            await message.delete()
        if message.content.lower() == '!setchannel':
            with open('targetchannel.txt', "w") as myfile:
                myfile.write(str(message.channel.id))
            await message.channel.send('target channel id set')

    # vérifie que le message n'est pas un lien (pour éviter les boucle sur les trigger words)
    if not 'http' in message.content.lower():
        if message.content.lower() in checker:
            for x in range(len(files)):
                await gifprint(message, message.content.lower(), messages[x], gifs[x], 0, ranarray[x])

        else:
            if message.content.lower()[0] == '$':
                data = json.loads(urllib.request.urlopen(
                    "http://api.giphy.com/v1/gifs/search?q=" + message.content.lower().replace(' ',
                                                                                               '+') + "&api_key=" + str(
                        GIPHYTOKEN)).read())
                if len(data["data"]) > 5:
                    await message.channel.send(data["data"][random.randint(0, 5)]["embed_url"])
                else:
                    await message.channel.send(data["data"][random.randint(0, len(data["data"]) - 1)]["embed_url"])


@tasks.loop(seconds=1.0)
async def loop():
    if target ==True:
        # envoi un message a une heure donnée
        channel = client.get_channel(int(targetchannelid[0]))
        msg = timedmessages()
        if msg != '':
            await channel.send(msg)


@loop.before_loop
async def before():
    await client.wait_until_ready()


loop.start()

client.run(DISCORDTOKEN)