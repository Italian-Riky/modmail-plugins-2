import asyncio
import emoji
import re
import typing

import discord
from discord.ext import commands

from core import checks
from core.models import PermissionLevel

class UnicodeEmoji(commands.Converter):
    async def convert(self, ctx, argument):
        if argument in emoji.UNICODE_EMOJI:
            return discord.PartialEmoji(name=argument, animated=False)
        raise commands.BadArgument('Emoji non riconosciuta')

Emoji = typing.Union[discord.PartialEmoji, discord.Emoji, UnicodeEmoji]

class ReactionRoles(commands.Cog):
    """Assegna ruoli ai tuoi membri con delle semplicissime reazioni! (Plugin tradotto da [Italian Riky](https://github.com/Italian-Riky])"""

    def __init__(self, bot):
        self.bot = bot
        self.db = bot.plugin_db.get_partition(self)
        
    @commands.group(name="reactionrole", aliases=["rr"], invoke_without_command=True)
    @checks.has_permissions(PermissionLevel.ADMINISTRATOR)
    async def reactionrole(self, ctx: commands.Context):
        """Assegna ruoli ai tuoi membri con delle semplicissime reazioni!"""
        await ctx.send_help(ctx.command)
        
    @reactionrole.command(name="add", aliases=["make"])
    @checks.has_permissions(PermissionLevel.ADMINISTRATOR)
    async def rr_add(self, ctx, message: str, role: discord.Role, emoji: Emoji,
                     ignored_roles: commands.Greedy[discord.Role] = None):
        """
        Imposta i Reaction roles.
        - Nota:
        Puoi usare un'emoji alla volta, ma potrai sempre aggiungerne altre di differenti!.
        - Uso:
        Invia un messaggio in qualsiasi categoria visibile al bot, Copia l'ID Del messaggio, E usa il comando
        {prefix}reactionrole add MESSAGE_ID @ruolo :emoji:
        
        [Per copiare l'ID Del messaggio devi attivare la [modalità sviluppatore!](https://hastebin.com/raw/ojuhekucer)]
        """
        emote = emoji.name if emoji.id is None else str(emoji.id)
        message_id = int(message.split("/")[-1])
        
        for channel in ctx.guild.text_channels:
            try:
                message = await channel.fetch_message(message_id)
            except (discord.NotFound, discord.HTTPException, discord.Forbidden):
                message = None
                continue
            else:
                break
                
        if not message:
            return await ctx.send("⛔|Messaggio non trovato.")
        
        if ignored_roles:
            blacklist = [role.id for role in ignored_roles]
        else:
            blacklist = []
            
        await self.db.find_one_and_update(
            {"_id": "config"}, {"$set": {emote: {"role": role.id, "msg_id": message.id, "ignored_roles": blacklist, "state": "unlocked"}}},
            upsert=True)
        
        await message.add_reaction(emoji)
        await ctx.send("✅|Reaction Role impostato con successo!")
        
    @reactionrole.command(name="remove", aliases=["delete"])
    @checks.has_permissions(PermissionLevel.ADMINISTRATOR)
    async def rr_remove(self, ctx, emoji: Emoji):
        """Elimina il reaction Role."""
        emote = emoji.name if emoji.id is None else str(emoji.id)
        config = await self.db.find_one({"_id": "config"})
        
        valid, msg = self.valid_emoji(emote, config)
        if not valid:
            return await ctx.send(msg)
            
        await self.db.find_one_and_update({"_id": "config"}, {"$unset": {emote: ""}})
        await ctx.send("✅|Reaction Role rimosso con successo!.")
        
    @reactionrole.command(name="lock", aliases=["pause", "stop"])
    @checks.has_permissions(PermissionLevel.ADMINISTRATOR)
    async def rr_lock(self, ctx, emoji: Emoji):
        """
        Disabilita temporaneamente un reaction role!.
         - Esempio:
        `{prefix}rr lock 👀`
        """
        emote = emoji.name if emoji.id is None else str(emoji.id)
        config = await self.db.find_one({"_id": "config"})
        
        valid, msg = self.valid_emoji(emote, config)
        if not valid:
            return await ctx.send(msg)
        
        config[emote]["state"] = "locked"
        
        await self.db.find_one_and_update(
        {"_id": "config"}, {"$set": {emote: config[emote]}}, upsert=True)
        await ctx.send("✅|Reaction role disattivato con successo!.")
        
    @reactionrole.command(name="unlock", aliases=["resume"])
    @checks.has_permissions(PermissionLevel.ADMINISTRATOR)
    async def rr_unlock(self, ctx, emoji: Emoji):
        """
        Sblocca un reaction role disattivato precedentemente.
         - Esempio:
        `{prefix}rr unlock 👀`
        """
        emote = emoji.name if emoji.id is None else str(emoji.id)
        config = await self.db.find_one({"_id": "config"})
        
        valid, msg = self.valid_emoji(emote, config)
        if not valid:
            return await ctx.send(msg)

        config[emote]["state"] = "unlocked"
        
        await self.db.find_one_and_update(
        {"_id": "config"}, {"$set": {emote: config[emote]}}, upsert=True)
        await ctx.send("✅|Reaction Role sbloccato con successo!")
            
#     @reactionrole.command(name="make")
#     @checks.has_permissions(PermissionLevel.ADMINISTRATOR)
#     async def rr_make(self, ctx):
#         """
#         Crea un reaction Role in modo interattivo!
#         Nota: Puoi mettere una reazione alla volta, ma poi ne puoi mettere multiple!
#         """

#         # checks 
#         def check(msg):
#             return ctx.author == msg.author and ctx.channel == msg.channel

#         def channel_check(msg):
#             return check(msg) and len(msg.channel_mentions) != 0

#         def emoji_and_role_check(msg):
#             return check(msg) and (discord.utils.get(ctx.guild.roles, name=msg.content.strip()[1:].strip()) is not None and 
        
#         # getting the values (inputs) from the user
#         await ctx.send("Allora, In che canale vuoi che sia mandato l'annuncio? (Assicurati di menzionare il canale)")
#         try:
#             channel_msg = await self.bot.wait_for("message", check=channel_check, timeout=30.0)
#             channel = channel_msg.channel_mentions[0]
#         except asyncio.TimeoutError:
#             return await ctx.send("Troppo tardi! Il reaction role è stato cancellato.", delete_after=10.0)
#         await ctx.send(f"Ok, Quindi il canale è {channel.mention}. Cosa vuoi che sia scritto nel messaggio? Usa | Per separare il titolo "
#                         "dalla descrizione!\n **Esempio:** `Questo è il titolo. | Questa è la descrizione!`")
#         try:
#             title_and_description = await self.bot.wait_for("message", check=check, timeout=120.0)
#             title = ("".join(title_and_description.split("|", 1)[0])).strip()
#             description = ("".join(title_and_description.split("|", 1)[1])).strip()
#         except asyncio.TimeoutError:
#             return await ctx.send("Troppo tardi!il reaction role è stato cancellato.", delete_after=10.0)
                
#         await ctx.send("Bene! Vuoi che il tuo messaggio sia colorato? rispondi con un codice esadecimale se lo desideri o se non lo fai "
#                        f"Type `{ctx.prefix}none`\nSono confuso, che codice hex è questo? Guarda su https://htmlcolorcodes.com/color-picker/")
#         # getting a valid hex
#         valid_hex = False                      
#         while not valid_hex:
#             try:
#                 hex_code = await self.bot.wait_for("message", check=check, timeout=60.0)
#                 if hex_code.content.lower() == "none" or hex_code.content.lower() == f"{ctx.prefix}none":
#                     color = self.bot.main_color
#                     break
#                 valid_hex = re.search(r"^#(?:[0-9a-fA-F]{3}){1,2}$", hex_code.content)
#             except asyncio.TimeoutError:
#                 return await ctx.send("Troppo tardi! Il reaction role è stato cancellato.", delete_after=10.0)
#             if not valid_hex:
#                 embed = discord.Embed(description="""Questo non sembra un valido codice hex!!
#                                                    Perfavore metti un **valido** [Codice hex](https://htmlcolorcodes.com/color-picker)""")
#                 await ctx.send(embed=embed)
#             else:
#                 color = hex_code.content.replace("#", "0x")

#         # Crea l'embed e mandalo all'utente
#         embed = discord.Embed(title=title, description=description, timestamp=datetime.datetime.utcnow(), color=color)
#         await ctx.send("Bene! L'embed ora assomiglia a questo:", embed=embed)
        

#         await ctx.send("L'ultimo passo è la scelta delle emoji, Il formato per aggiugere le emoji è: :emoji: @ruolo "
#                        f"Quando sei pronto scrivi `{ctx.prefix}done`\n**Esempio:** `🎉 Pizzoccheri`")
#         emojis = []
#         roles = []

#         while True:
#             try:
#                 emoji_and_role = await self.bot.wait_for("message", check=emoji_and_role_check, timeout=60.0)
#             except asyncio.TimeoutError:
#                 return await ctx.send("Troppo tardi! Il reaction role è stato cancellato.", delete_after=10.0)
#             else:
#                 if emoji_and_role.content.lower() == "done" or emoji_and_role.content.lower() == f"{ctx.prefix}done":
#                     if len(roles) == 0:
#                         await ctx.send("Devi specificare almeno un ruolo per reaction role.")
#                     else:
#                        break
#                 else:
#                     emoji = emoji_and_role.content[0]
#                     role = emoji_and_role.content[1:].strip()
#                     if ...
                  

    @reactionrole.group(name="blacklist", aliases=["ignorerole"], invoke_without_command=True)
    @checks.has_permissions(PermissionLevel.ADMINISTRATOR)
    async def blacklist(self, ctx):
        """Ignora alcuni ruoli dal Reaction Role."""
        await ctx.send_help(ctx.command)
        
    @blacklist.command(name="add")
    @checks.has_permissions(PermissionLevel.ADMINISTRATOR)
    async def blacklist_add(self, ctx, emoji: Emoji, roles: commands.Greedy[discord.Role]):
        """Ignora alcuni ruoli dalla reazione."""
        emote = emoji.name if emoji.id is None else str(emoji.id)
        config = await self.db.find_one({"_id": "config"})
        valid, msg = self.valid_emoji(emote, config)
        if not valid:
            return await ctx.send(msg)
        
        blacklisted_roles = config[emote]["ignored_roles"] or []
        
        new_blacklist = [role.id for role in roles if role.id not in blacklisted_roles]
        blacklist = blacklisted_roles + new_blacklist
        config[emote]["ignored_roles"] = blacklist
        await self.db.find_one_and_update(
            {"_id": "config"}, {"$set": {emote: config[emote]}}, upsert=True)
        
        ignored_roles = [f"<@&{role}>" for role in blacklist]
        
        embed = discord.Embed(title="✅|Ruolo messo nella blacklist con successo!.", color=discord.Color.green())
        try:
            embed.add_field(name=f"Ruoli correnti ignorati da {emoji}", value=" ".join(ignored_roles))
        except HTTPException:
            pass
        await ctx.send(embed=embed)
        
    @blacklist.command(name="remove")
    @checks.has_permissions(PermissionLevel.ADMINISTRATOR)
    async def blacklist_remove(self, ctx, emoji: Emoji, roles: commands.Greedy[discord.Role]):
        """Permetti ad alcuni ruoli di reagire al messaggio anche se nella blacklist."""
        emote = emoji.name if emoji.id is None else str(emoji.id)
        config = await self.db.find_one({"_id": "config"})
        valid, msg = self.valid_emoji(emote, config)
        if not valid:
            return await ctx.send(msg)
        
        blacklisted_roles = config[emote]["ignored_roles"] or []
        blacklist = blacklisted_roles.copy()
        
        [blacklist.remove(role.id) for role in roles if role.id in blacklisted_roles]
        config[emote]["ignored_roles"] = blacklist
        
        await self.db.find_one_and_update(
            {"_id": "config"}, {"$set": {emote: config[emote]}}, upsert=True)
        
        ignored_roles = [f"<@&{role}>" for role in blacklist]
        
        embed = discord.Embed(title="✅|Ruolo rimosso dalla blacklist con successo!", color=discord.Color.green())
        try:
            embed.add_field(name=f"Ruoli ignorati nella blacklist in questo momento per {emoji}", value=" ".join(ignored_roles))
        except:
            pass
        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if not payload.guild_id:
            return
        
        config = await self.db.find_one({"_id": "config"})
        
        emote = payload.emoji.name if payload.emoji.id is None else str(payload.emoji.id)
        emoji = payload.emoji.name if payload.emoji.id is None else payload.emoji
        
        guild = self.bot.get_guild(payload.guild_id)
        member = discord.utils.get(guild.members, id=payload.user_id)
        
        if member.bot:
            return
        
        try:
            msg_id = config[emote]["msg_id"]
        except (KeyError, TypeError):
            return
        
        if payload.message_id != int(msg_id):
            return
        
        ignored_roles = config[emote].get("ignored_roles")
        if ignored_roles:
            for role_id in ignored_roles:
                role = discord.utils.get(guild.roles, id=role_id)
                if role in member.roles:
                    await self._remove_reaction(payload, emoji, member)
                    return
        
        state = config[emote].get("state", "unlocked")
        if state and state == "locked":
            await self._remove_reaction(payload, emoji, member)
            return
        
        rrole = config[emote]["role"]
        role = discord.utils.get(guild.roles, id=int(rrole))

        if role:
            await member.add_roles(role)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        if payload.guild_id is None:
            return
        
        config = await self.db.find_one({"_id": "config"})
        emote = payload.emoji.name if payload.emoji.id is None else str(payload.emoji.id)
        
        try:
            msg_id = config[emote]["msg_id"]
        except (KeyError, TypeError):
            return
                                                              
        if payload.message_id == int(msg_id):
            guild = self.bot.get_guild(payload.guild_id)
            rrole = config[emote]["role"]
            role = discord.utils.get(guild.roles, id=int(rrole))

            if role:
                member = discord.utils.get(guild.members, id=payload.user_id)
                await member.remove_roles(role)
                
    async def _remove_reaction(self, payload, emoji, member):
        channel = self.bot.get_channel(payload.channel_id)
        msg = await channel.fetch_message(payload.message_id)
        reaction = discord.utils.get(msg.reactions, emoji=emoji)
        await reaction.remove(member)
                                  
    def valid_emoji(self, emoji, config):
        try:
            emoji = config[emoji]
            return True, None
        except (KeyError, TypeError):
            return False, "⛔|Non c'è nessun reaction role impostato con questa emoji!"
                
def setup(bot):
    bot.add_cog(ReactionRoles(bot))
