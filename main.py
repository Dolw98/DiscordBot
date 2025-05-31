import os
import discord
from discord.ext import commands
from discord.ui import View, Select
from googletrans import Translator
from flask import Flask
from threading import Thread

# -------------------------------
# FLASK SERVER (UptimeRobot alive)
# -------------------------------

app = Flask('')

@app.route('/')
def home():
    return "✅ Bot is actief!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# -------------------------------
# DISCORD BOT INSTELLINGEN
# -------------------------------

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

translator = Translator()

LANGUAGES = {
    "🇬🇧 English": "en",
    "🇵🇹 Português": "pt",
    "🇰🇷 한국인": "ko",
    "🇹🇼 繁體中文": "zh-TW",
    "🇯🇵 日本語": "ja",
    "🇪🇸 Español": "es",
    "🇫🇷 Français": "fr",
    "🇩🇪 Deutsch": "de",
}

class TranslateDropdown(discord.ui.Select):
    def __init__(self, message_content):
        self.message_content = message_content

        options = [
            discord.SelectOption(label=label, value=lang_code)
            for label, lang_code in LANGUAGES.items()
        ]

        super().__init__(
            placeholder="🌍 Choose language...",
            min_values=1,
            max_values=1,
            options=options
        )

    async def callback(self, interaction: discord.Interaction):
        lang_code = self.values[0]
        try:
            # Vind het juiste vlag-label
            label = next(k for k, v in LANGUAGES.items() if v == lang_code)

            # Vertalen (LET OP: await vereist in jouw omgeving!)
            translated = await translator.translate(self.message_content, dest=lang_code)

            # Stuur compacte vertaling terug
            await interaction.response.send_message(
                f"{label} → {translated.text}",
                ephemeral=True
            )

        except Exception as e:
            await interaction.response.send_message(
                f"❌ Fout bij vertalen: {e}",
                ephemeral=True
            )

class TranslateView(View):
    def __init__(self, message_content):
        super().__init__(timeout=None)
        self.add_item(TranslateDropdown(message_content))

@bot.event
async def on_ready():
    print(f"✅ Bot actief als {bot.user}")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    view = TranslateView(message.content)
    await message.channel.send(view=view)
    await bot.process_commands(message)

# -------------------------------
# START BOT
# -------------------------------

keep_alive()  # Houdt Replit wakker
bot.run(os.getenv("DISCORD_TOKEN"))
