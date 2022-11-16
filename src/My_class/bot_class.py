import sys
import os
import clipboard

import discord
from discord.ext import commands
import My_class.keyboardTool as keyboardTool
from discord.ui import View

from PIL import ImageGrab

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


save_path = resource_path("temp.png")

def img_save():
    img = ImageGrab.grab()
    img.save(save_path)

class Key_view(View):
    @discord.ui.button(label="키 목록", style=discord.ButtonStyle.red)
    async def button_key_list_callback(self, button, Interaction):
        message = """```
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
        await Interaction.response.send_message(message)
    
    @discord.ui.button(label="키 입력 방법", style=discord.ButtonStyle.red)
    async def button_key_help_callback(self, button, Interaction):
        message = """
.k (key) = 키 하나 입력
.ks (문자) = 문자 입력
.dk (key) (key) = 키 두개 동시 입력(ex ctrl + a)
        """
        await Interaction.response.send_message(message)


class Help_view(View):
    @discord.ui.button(label="키 도움말", style=discord.ButtonStyle.grey)
    async def button_key_callback(self, button, Interaction):
        await Interaction.response.send_message(view = Key_view())
    
    @discord.ui.button(label="화면", style=discord.ButtonStyle.green)
    async def button_screen_callback(self, button, Interaction):
        img_save()
        await Interaction.response.send_message("스크린샷", file = discord.File(save_path))

    @discord.ui.button(label="컴퓨터 끄기", style=discord.ButtonStyle.red)
    async def button_off_callback(self, button, Interaction):
        os.system("shutdown -s -t 3")
        await Interaction.response.send_message("컴퓨터를 종료합니다.")


class discord_bot():
    def __init__(self, bot_token):
        self.bot_token = bot_token
        intents = discord.Intents.default()        
        intents.message_content = True
        self.bot = commands.Bot(command_prefix=".", intents=intents)
    

    def token_set(self, bot_token):
        self.bot_token = bot_token
    
    def start(self):
        @self.bot.command()
        async def h(ctx):
            await ctx.send("도움말", view = Help_view())

        @self.bot.command()
        async def k(ctx, arg1 : str):
            """
            키 하나만 누를때
            """
            keyboardTool.press(arg1)
            img_save()
            await ctx.send("screen",file = discord.File(save_path))
        
        @self.bot.command()
        async def ks(ctx, arg1 : str):
            """
            문자열 입력할때
            """
            clipboard.copy(arg1)
            keyboardTool.pressAndHold("ctrl")
            keyboardTool.press("v")
            keyboardTool.release("ctrl")
            img_save()
            await ctx.send("screen", file = discord.File(save_path))

        @self.bot.command()
        async def dk(ctx, arg1 : str, arg2 : str):
            """
            키 두개 같이 누를때(ex ctrl + a)
            """
            keyboardTool.pressAndHold(arg1)
            keyboardTool.press(arg2)
            keyboardTool.release(arg1)
            img_save()
            await ctx.send("screen",file = discord.File(self.save_path))
                
        self.bot.run(self.bot_token)
       
    def stop(self):
        self.bot.loop.stop()