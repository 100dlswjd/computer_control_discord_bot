import discord
import sys
import os
import time

from threading import Thread, Event
from discord.ext import commands
import My_class.keyboardTool as keyboardTool

from PIL import Image
from PIL import ImageGrab
from PIL import ImageDraw


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class discord_bot():
    def __init__(self, bot_token):
        self.bot_token = bot_token
        self.save_path = resource_path("temp.png")
        intents = discord.Intents.default()        
        intents.message_content = True
        self.bot = commands.Bot(command_prefix=">", intents=intents)

    def token_set(self, bot_token):
        self.bot_token = bot_token
    
    def img_save(self):
        img = ImageGrab.grab()
        img.save(self.save_path)

    def start(self):
        @self.bot.command()
        async def screen(ctx):
            self.img_save()
            await ctx.send("screen", file = discord.File(self.save_path))
            
        @self.bot.command()
        async def h(ctx):
            message = """
h = 명령어 도움말
s = 화면 스크린샷
p = 키보드 입력
dk = 키보드 두개 같이 입력(ex ctrl + a)
off = 컴퓨터 종료
        """
            await ctx.send(message)

        @self.bot.command()
        async def s(ctx):
            """
            화면 스크린샷
            """
            self.img_save()
            await ctx.send("screen",file = discord.File(self.save_path))

        @self.bot.command()
        async def p(ctx, arg1 : str):
            """
            키 하나만 누를때
            """
            keyboardTool.press(arg1)
            self.img_save()
            await ctx.send("screen",file = discord.File(self.save_path))

        @self.bot.command()
        async def dk(ctx, arg1 : str, arg2 : str):
            """
            키 두개 같이 누를때(ex ctrl + a)
            """
            keyboardTool.pressAndHold(arg1)
            keyboardTool.press(arg2)
            keyboardTool.release(arg1)
            self.img_save()
            await ctx.send("screen",file = discord.File(self.save_path))

        @self.bot.command()
        async def off(ctx):
            os.system("shutdown -s -t 3")
            await ctx.send("컴퓨터 종료")
                
        self.bot.run(self.bot_token)
       
    def stop(self):
        self.bot.loop.stop()