import discord
from discord import bot
from discord.ext import commands
from discord.commands import slash_command
import asyncio


class ticketsystem(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.add_view(ticketing())
        self.bot.add_view(closeticket())

    @slash_command(description="Erstelle das Ticket System")
    @discord.default_permissions(administrator=True)
    async def ticket_system(self, ctx):
        embed = discord.Embed(
            title="**Erstelle ein Ticket!**",
            description="Der Support ist die Schnittstelle von der Community und den Membern",
            color= discord.Color.green()
        )
        embed.add_field(name="Stelle eine Frage...", value="Wenn du eine Allgemiene Frage zum Server oder zu Discord hast, bist du hier genau richtig!", inline=False)
        embed.add_field(name="Beantrage deine Vorteile oder Gewinne...", value="Hier kannst du deine Vorteile von Boosts oder Gewinne von einem Giveaway beantragen!", inline=False)
        embed.add_field(name="Melde einen Member...", value="Dir ist etwas auf dem Server aufgefallen, was gegen die Regeln verstöst? Melde den Member hier und erhalte ein Cosmetik!", inline=False)
        embed.add_field(name="Hole dir Infos...", value="Du bist Neu auf Discord? Erkundige dich jederzeit über neue Funktionen und Updates!", inline=False)
        await ctx.respond(embed=embed, view=ticketing())
        bot.persistent_view_added = False


def setup(bot: discord.Bot):
    bot.add_cog(ticketsystem(bot))


class ticketing(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.select(custom_id="ticketing", placeholder="Ticket Öffnen", min_values=1, max_values=1, options=[discord.SelectOption(label="Frage", description="Stelle eine frage zum Server oder Discord", emoji="❓"), discord.SelectOption(label="Report", description="Melde einen Member", emoji="🚫"), discord.SelectOption(label="Bestellen", description="Gebe eine Bestellung auf!", emoji="<:paypal:1229390966859759616>"), discord.SelectOption(label="Bewerben", description="Bewerbe dich gerne hier!", emoji="<a:CatJamDisco:1171749567855869982>")]) #Füge weitere Tickets hinzu
    async def callback(self, select, interaction):
        overwrites = {interaction.guild.default_role: discord.PermissionOverwrite(view_channel=False), interaction.user: discord.PermissionOverwrite(view_channel=True, send_messages=True, embed_links=True), interaction.guild.me: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True)}
        channel = await interaction.guild.create_text_channel(f"ticket-{interaction.user.name}", overwrites=overwrites, reason=f"Ticket für {interaction.user.name}")
        await interaction.response.send_message(f"Ticket erstellt: {channel.mention}", ephemeral=True)
        if select.values[0] == "Frage":
            await channel.send(f"Hallo {interaction.user.mention}! Du hast eine Frage zum Server oder zu Discord? Denn teile uns diese gerne mit! Ein Teammitglied wird sich in kürze bei dir melden und dir deine Frage beantworten", view=closeticket())
        elif select.values[0] == "Report": #Wenn du weitere Ticktes hinzugefügt hast, musst du auch eine message mit elif hinzufügen
            await channel.send(f"Hallo {interaction.user.mention}, um einen anderen Member reporten zu können benötigen wir beweise in form von Screenshots oder Aufnahmen. Wir werden uns schnellstmöglich bei dir melden!", view=closeticket())
        elif select.values[0] == "Bestellen":
            await channel.send(f"Hallo {interaction.user.mention}! Du hast dir ein Produkt ausgesucht? Denn teile uns dieses mit. Ein Teammitglied wird sich schnellstmöglich bei dir melden", view=closeticket())
        elif select.values[0] == "Bewerben":
            await channel.send(f"Hallo {interaction.user.mention}, wir freuen uns das du ein Teil unseres Teams werden willst. Schreibe deine Bewerbung gerne hier hinein und ein Teammitglied wird sich schnellstmöglich bei dir melden", view=closeticket()) #Wenn du weitere Ticktes hinzugefügt hast, musst du auch eine message mit elif hinzufügen
        


class closeticket(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(custom_id="closebutton", label="Ticket schließen", style=discord.ButtonStyle.danger, emoji="🔒")
    async def button_callback(self, button, interaction):
        await interaction.response.send_message("Ticket wird geschlossen...")
        await asyncio.sleep(2)
        await interaction.channel.delete()
        await asyncio.sleep(10)
        embed = discord.Embed(
            title="Dein Ticket wurde Geschlossen",
            description="Danke das du ein Ticket auf dem Server von Leon gezogen hast. Wenn du ein weiteres Ticket Öffnen willst, gehe gerne in den Support Kanal",
            color= discord.Color.green()
        )
        await interaction.user.send(embed=embed)
