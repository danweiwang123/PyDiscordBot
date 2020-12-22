import discord
from discord.ext import commands
import random
import os
import datetime
import re

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from PIL import Image
from dotenv import load_dotenv
token ='insert token'
#path to chromedriver
weatherpath = "/chromedriver.exe"
#direct path to meme folder
memepath = ""
client = commands.Bot(command_prefix = '!')

client = discord.Client()




def crop(image_path, coords, saved_location):
    """
    @param image_path: The path to the image to edit
    @param coords: A tuple of x/y coordinates (x1, y1, x2, y2)
    @param saved_location: Path to save the cropped image
    """
    image_obj = Image.open(image_path)
    cropped_image = image_obj.crop(coords)
    cropped_image.save(saved_location)

@client.event
async def on_ready():
    print('Bot is ready.')  

#@client.event
#async def on_member_remove(member):
 #   await member.create_dm()
  #  await member.dm_channel.send(f'{member.name} is Baka.')

@client.event
async def on_member_join(member):
    print(member)
    print(type(member))
    await member.create_dm()
    await member.dm_channel.send(f'Welcome home to Sobaa master {member.name}')


@client.event
async def on_message(message):
    #checks if user messages and not a bot
    if message.author == client.user:
        return
    command = message.content.split()
    if "!weather" == command[0]:
        await message.channel.send('please wait one moment')
        #Setting up Chromium Settings
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--headless") 
        
        urls = re.search('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', 'https://www.theweathernetwork.com/ca/weather/ontario/toronto')
        #Selenium ScreenShot
        driver=webdriver.Chrome(options=chrome_options,executable_path=weatherpath)
        driver.get(urls.group())
        driver.set_window_size(1920, 1080)    
        driver.get_screenshot_as_file('screenshot.png')
        crop('screenshot.png', (300, 184, 1000, 700), 'screenshot.png')
        await message.channel.send(file=discord.File('screenshot.png'))
        #await message.channel.send(f"<@{message.author.id}> Heres Your ScreenShot Of: {urls.group()}")
        os.remove('screenshot.png')
        driver.quit()
    #roll a dice
    if  command[0] == "!roll":
        roll = random.randint(1,6)
        sender = str(message.author)
        msg = (sender[:len(sender)-5] + ' rolled a '+ str(roll))
        await message.channel.send(msg)
    #flip a coin
    if command[0] == '!coinflip':
        coin = random.randint(0,1)
        if (coin == 0 ):
            result = 'tails'
        elif (coin == 1):
            result = 'heads'
        await message.channel.send(result)
    #generate a random number 
    if command[0] == '!rng':
        try:
            result = random.randint(1,int(command[1]))
            await message.channel.send(result)
        except:
            await message.channel.send('please enter a valid parameter')
    #sends a meme from meme server
    if command[0] == '!meme':
        files = os.listdir(memepath)
        pic = discord.File(memepath+"\\"+random.choice(files))
        await message.channel.send(file=pic)
        #os.remove(pic)
    if command[0] == '!help':
        await message.channel.send("""
        ```Commands:
\n!weather [Gets the weather]
\n!roll [rolls a dice]
\n!coinflip [flips a coin]
\n!rng x [generates a random number from 1 to x]
\n!meme [sends a random meme]```""")
    
client.run(token)
