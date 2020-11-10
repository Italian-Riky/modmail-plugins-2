import re
import typing

from types import SimpleNamespace

import discord
from discord.ext import commands

from core import checks
from core.models import PermissionLevel

class Role(commands.Cog):
    """Crea ruoli e aggiungili facilmente ai tuoi membri (plugin tradotto da [Italian Riky](https://github.com/Italian-Riky))."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @checks.has_permissions(PermissionLevel.ADMINISTRATOR)
    async def role(self, ctx, role: discord.Role, member: discord.Member=None):
        """Assegna un ruolo a un membro."""
        if member is None:
            try:
                member = ctx.guild.get_member(int(ctx.channel.topic[9:]))
            except (ValueError, TypeError):
                raise commands.MissingRequiredArgument(SimpleNamespace(name="role"))
        
        if role.position > ctx.author.roles[-1].position:
            return await ctx.send("Non hai il permesso per dare questo ruolo!.")
        
        await member.add_roles(role)
        await ctx.send(f"Aggiunto con successo il ruolo a {member.name}!")

    @commands.command()
    @checks.has_permissions(PermissionLevel.ADMINISTRATOR)
    async def unrole(self, ctx, role: discord.Role, member: discord.Member=None):
        """Rimuovi un ruolo ad un membro."""
        if member is None:
            try:
                member = ctx.guild.get_member(int(ctx.channel.topic[9:]))
            except (ValueError, TypeError):
                raise commands.MissingRequiredArgument(SimpleNamespace(name="unrole"))
            
        if role.position > ctx.author.roles[-1].position:
            return await ctx.send("Non hai il permesso di rimuovere questo ruolo.")
        
        await member.remove_roles(role)
        await ctx.send(f"Rimosso con successo il ruolo a {member.name}!")

    @commands.command(aliases=["makerole"])
    @checks.has_permissions(PermissionLevel.ADMINISTRATOR)
    async def createrole(self, ctx, name: str, color: str):
        """create a role."""
        color = "#" + color.strip("#")
        
        valid = re.search(r"^#(?:[0-9a-fA-F]{3}){1,2}$", color)
        if not valid:
            embed = discord.Embed(title="Errore", color=self.bot.main_color,
                description="Inserisci un **valido [hex code](https://htmlcolorcodes.com/color-picker)**")
            return await ctx.send(embed=embed)

        await ctx.guild.create_role(name=name, color=discord.Color(int(color.replace("#", "0x"), 0)))
        await ctx.send("Ruolo creato con successo!")

def setup(bot):
    bot.add_cog(Role(bot))
    
