import os
import discord
from discord.ext import commands
from googletrans import Translator

# Initialiseer intents en bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Initialiseer vertaler
translator = Translator()

# Ondersteunde talen
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

# View en dropdown voor vertaling
class TranslateDropdown(discord.ui.Select):
    def __init__(self, message_content):
        self.message_content = message_content
        options = [
            discord.SelectOption(label=label, value=lang_code)
            for label, lang_code in LANGUAGES.items()
        ]
        super().__init__(placeholder="🌍 Kies taal...", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        lang_code = self.values[0]
        try:
            label = next(k for k, v in LANGUAGES.items() if v == lang_code)
            translated = await bot.loop.run_in_executor(None, lambda: translator.translate(self.message_content, dest=lang_code))
            await interaction.response.send_message(
                f"{label} → {translated.text}", ephemeral=True
            )
        except Exception as e:
            await interaction.response.send_message(
                f"❌ Fout bij vertalen: {e}", ephemeral=True
            )

class TranslateView(discord.ui.View):
    def __init__(self, message_content):
        super().__init__(timeout=None)
        self.add_item(TranslateDropdown(message_content))

# Event handlers
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

# Start de bot
bot.run(os.getenv("DISCORD_TOKEN"))

