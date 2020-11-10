import datetime

import discord
from discord.ext import commands

from core import checks
from core.models import PermissionLevel

class Report(commands.Cog): 
    """Un modo semplice per i tuoi membri di segnalare un cattivo comportamento (Plugin tradotto da [Italian Riky](https://github.com/Italian-Riky))"""
    
    def __init__(self, bot):
        self.bot = bot
        self.db = bot.plugin_db.get_partition(self)

    @commands.command(aliases=["rchannel"])
    @checks.has_permissions(PermissionLevel.MODERATOR)
    async def reportchannel(self, ctx, channel: discord.TextChannel):
        """Imposta il canale delle segnalazioni"""
        await self.db.find_one_and_update({"_id": "config"}, {"$set": {"report_channel": channel.id}}, upsert=True)
        
        embed = discord.Embed(color=discord.Color.blue(), timestamp=datetime.datetime.utcnow())
        embed.add_field(name="Imposta il canale", value=f"Impostato il canale {channel.mention} per le segnalazioni con successo!", inline=False)
        
        await ctx.send(embed=embed)

    @commands.command(aliases=["rmention"])
    @checks.has_permissions(PermissionLevel.MODERATOR)
    async def reportmention(self, ctx, *, mention: str):
        """Imposta la menzione per le segnalazioni"""
        await self.db.find_one_and_update({"_id": "config"}, {"$set": {"report_mention": mention}}, upsert=True)
        
        embed = discord.Embed(color=discord.Color.blue(), timestamp=datetime.datetime.utcnow())
        embed.add_field(name="Menzione cambiata", value=f"Cambiata con {mention}!", inline=False)
        
        await ctx.send(embed=embed)

    @commands.command()
    async def report(self, ctx, user: discord.Member, *, reason: str):
        """Segnala il cattivo comportamento del membro"""
        config = await self.db.find_one({"_id": "config"})
        report_channel = config["report_channel"]
        setchannel = discord.utils.get(ctx.guild.channels, id=int(report_channel))
        
        try:
            report_mention = config["report_mention"]
        except KeyError:
            report_mention = ""
            
        embed = discord.Embed(color=discord.Color.red(), timestamp=datetime.datetime.utcnow())
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        
        embed.add_field(name="Persona Segnalata", value=f"{user.mention} | ID: {user.id}", inline=False)
        embed.add_field(name="Segnalata da:", value=f"{ctx.author.mention} | ID: {ctx.author.id}", inline=False)
        embed.add_field(name="Canale", value=ctx.channel.mention, inline=False)
        embed.add_field(name="Motivo", value=reason, inline=False)

        await setchannel.send(report_mention, embed=embed)
        await ctx.send("Persona segnalata con successo!")
                        
def setup(bot):
    bot.add_cog(Report(bot))
