import sys
import os

import discord
from discord.ext import commands
import My_class.keyboardTool as keyboardTool

from PIL import ImageGrab

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
>h = 명령어 도움말
>hk = 키 목록(좀 많음)
>s = 화면 스크린샷
>p (key)= 키보드 입력
>dk (key) (key)= 키보드 두개 같이 입력(ex ctrl + a)
>off = 컴퓨터 종료
        """
            await ctx.send(message)

        @self.bot.command()
        async def hk(ctx):
            message ="""```
backspace
tab
clear
enter
shift
ctrl
alt
pause
caps_lock
esc
spacebar
page_up
page_down
end
home
left_arrow
up_arrow
right_arrow
down_arrow
select
print
execute
print_screen
ins
del
help
0
1
2
3
4
5
6
7
8
9
a
b
c
d
e
f
g
h
i
j
k
l
m
n
o
p
q
r
s
t
u
v
w
x
y
z
numpad_0
numpad_1
numpad_2
numpad_3
numpad_4
numpad_5
numpad_6
numpad_7
numpad_8
numpad_9
multiply_key
add_key
separator_key
subtract_key
decimal_key
divide_key
f1
f2
f3
f4
f5
f6
f7
f8
f9
f10
f11
f12
num_lock
scroll_lock
left_shift
right_shift
left_control
right_control
left_menu
right_menu
browser_back
browser_forward
browser_refresh
browser_stop
browser_search
browser_favorites
browser_start_and_home
volume_mute
volume_Down
volume_up
next_track
previous_track
stop_media
play/pause_media
start_mail
select_media
start_application_1
start_application_2
attn_key
crsel_key
exsel_key
play_key
zoom_key
clear_key
+
,
-
.
/
`
;
[
\\
]
'
`
```"""
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