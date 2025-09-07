import discord, os, shutil, json
from discord.ext import commands

class Welcome(commands.Cog):
    
    def __init__(self, bot: discord.Bot, config_dir: str):
        self.bot = bot
        self.config_dir = config_dir
        self.config = json.loads(open(config_dir + "/config.json", "r"))
        if self.config["destination_channel_id"] == 0:
            print("[ERROR] Channel ID not set, disabling...")
            self.bot.remove_cog("Welcome")



def setup(bot: discord.Bot, config_dir: str = None):
    if config_dir is None:
        config_dir = globals().get('PLUGIN_CONFIG_DIR', '<unknown>')


    _, plugin_name = config_dir.split("/")

    if not os.path.exists(config_dir + "/config.json"):
        shutil.copy2(f"plugins/{plugin_name}/config.json", config_dir + "/config.json")

    
    bot.add_cog(Welcome(bot,config_dir))