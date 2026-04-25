import discord
from discord.ext import commands
from discord import app_commands
import datetime

# simple in-memory warnings system
warnings = {}

class Moderation(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # ---------------- WARN ----------------
    @app_commands.command(name="warn", description="Warn a user")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def warn(self, interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided"):
        uid = member.id

        if uid not in warnings:
            warnings[uid] = []

        warnings[uid].append(reason)

        await interaction.response.send_message(
            f"⚠️ {member.mention} warned.\nReason: {reason}"
        )

        try:
            await member.send(f"You were warned in {interaction.guild.name}\nReason: {reason}")
        except:
            pass

    # ---------------- KICK ----------------
    @app_commands.command(name="kick", description="Kick a user")
    @app_commands.checks.has_permissions(kick_members=True)
    async def kick(self, interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided"):
        await member.kick(reason=reason)
        await interaction.response.send_message(f"👢 Kicked {member.mention}\nReason: {reason}")

    # ---------------- BAN ----------------
    @app_commands.command(name="ban", description="Ban a user")
    @app_commands.checks.has_permissions(ban_members=True)
    async def ban(self, interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided"):
        await member.ban(reason=reason)
        await interaction.response.send_message(f"🔨 Banned {member.mention}\nReason: {reason}")

    # ---------------- TEMP MUTE (TIMEOUT) ----------------
    @app_commands.command(name="mute", description="Timeout a user for X minutes")
    @app_commands.checks.has_permissions(moderate_members=True)
    async def mute(self, interaction: discord.Interaction, member: discord.Member, minutes: int, reason: str = "No reason provided"):

        # calculate end time
        timeout_until = discord.utils.utcnow() + datetime.timedelta(minutes=minutes)

        # apply timeout
        await member.timeout(timeout_until, reason=reason)

        await interaction.response.send_message(
            f"🔇 {member.mention} muted for **{minutes} minutes**\nReason: {reason}"
        )

# ---------------- SETUP FUNCTION ----------------
async def setup(bot: commands.Bot):
    await bot.add_cog(Moderation(bot))