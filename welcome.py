import discord, os, shutil, json
from discord.ext import commands

class Welcome(commands.Cog):
    
    def __init__(self, bot: discord.Bot, config_dir: str):
        self.bot = bot
        self.config_dir = config_dir
        self.config = json.load(open(config_dir + "/config.json", "r"))
        if self.config["destination_channel_id"] == 0:
            print("[ERROR] Channel ID not set, disabling...")
            self.bot.remove_cog("Welcome")
    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        channel: discord.TextChannel = self.bot.get_channel(self.config["destination_channel_id"])
        if channel is None:
            print("[ERROR] Cannot get channel!")
        embed_data: dict = self.config["welcome_embed"]

        # Reemplazo de datos
        embed_data["title"] = embed_data["title"].replace("{user.name}", member.name)
        embed_data["title"] = embed_data["title"].replace("{user.id}", str(member.id))
        embed_data["title"] = embed_data["title"].replace("{user.mention}", f"<@{member.id}>")
        embed_data["description"] = embed_data["description"].replace("{user.name}", member.name)
        embed_data["description"] = embed_data["description"].replace("{user.id}", str(member.id))
        embed_data["description"] = embed_data["description"].replace("{user.mention}", f"<@{member.id}>")
        embed_data["outside"] = embed_data["outside"].replace("{user.name}", member.name)
        embed_data["outside"] = embed_data["outside"].replace("{user.id}", str(member.id))
        embed_data["outside"] = embed_data["outside"].replace("{user.mention}", f"<@{member.id}>")
        

        embed: discord.Embed = discord.Embed(title=embed_data["title"], description=embed_data["description"])
        if "color" in embed_data:
            embed.color = discord.Colour.from_rgb(embed_data["color"]["r"],embed_data["color"]["g"], embed_data["color"]["b"])
        if "footer" in embed_data:
            footer_data = embed_data["footer"]
            footer: discord.EmbedFooter = discord.EmbedFooter(footer_data["text"])
            if "icon_url" in footer_data:
                footer.icon_url = footer_data["icon_url"]
        if "fields" in embed_data:
            for field in embed_data["fields"]:
                embed.add_field(name=field["name"], value=field["value"], inline=field["inline"])
        





def setup(bot: discord.Bot, config_dir: str = None):
    if config_dir is None:
        config_dir = globals().get('PLUGIN_CONFIG_DIR', '<unknown>')


    _, plugin_name = config_dir.split("/")

    if not os.path.exists(config_dir + "/config.json"):
        shutil.copy2(f"plugins/{plugin_name}/config.json", config_dir + "/config.json")

    
    bot.add_cog(Welcome(bot,config_dir))