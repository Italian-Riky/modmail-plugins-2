import random

import discord
from discord.ext import commands

class Megadoot(commands.Cog):
    """
    Divertiti con questo plugin! (Plugin tradotto da [Italian Riky](https://github.com/Italian-Riky))
    """
    def __init__(self, bot):
        self.bot = bot
        self.fights = [
            '{0} ha provato a lanciare una palla di neve a {1} ma colpisce la macchina di Dabbit e Dabbit non è contento! ",
            "{0} placcato {1} con un pesce.",
            "{0} ha combattuto {1}, ma non è stato efficace ...",
            "{0} ha provato a lanciare un secchio d'acqua a {1}, ma l'ha gettato accidentalmente dappertutto {2}!",
            "{0} si è stancato dei giochi di parole di ks e ha cercato di combattere ma ha colpito accidentalmente {1}",
            "{0} ha provato a colpire {1}, ma {1} aveva una carta inversa nella manica, quindi {0} è stato colpito invece",
            "{0} ha cercato di combattere {1}, ma alla fine Dabbit ha ricevuto una zuppa di cereali.",
            "{0} ha tentato di attaccare {1}, ma sono scivolati e si sono schiantati contro l'auto di Ghoul, facendo un'enorme ammaccatura a forma di gatto sul cofano",
            "{0} ha cercato di combattere {1} ma è stato attaccato da una banda di gattini",
            "{0} ha sfidato {1} una gara in Mario Kart ma la CPU ha vinto invece!",
            "{1} ha schivato uno swing potente e raffinato da {0} e poi ha rovesciato {0} per legittima difesa.",
            "{0} ha implorato il proprio animale domestico di attaccare {1}, ma l'animale lo ha guardato senza alcuna indicazione di comprensione.",
            "{0} ha combattuto come un cane, ma {1} ha reagito come un orso, vincendo il combattimento!",
            'Appare un {1} selvaggio! \n {1} usa Bite! Non è molto efficace ... \n {0} usa Mega Punch! È molto efficace! \n {0} ha vinto! ",
            "Mentre {0} correva tutto sudato e stanco, allungando la mano per un ultimo pugno, {1} si precipitò di lato, lasciando {0} cadere a terra.",
            "{0} ha provato a modificare il Dupe Bomber 3000 per abbattere {1} con tonnellate di segnalazioni di stupidi, ma Dannysaur è arrivato per primo e li ha negati tutti ... il che ha rotto la macchina.",
            "{0} si è megaevoluto e ha cercato di eliminare {1} con Hyper Beam! Ma {1} ha usato Mimic e invece l'ha invertito su {0}! ",
            "{0} ha lanciato una palla di neve contro {1} ma sfortunatamente colpisce una finestra in Discord HQ. Ops ',
            "{0} ha indotto {1} a svegliare la pizza addormentata. The Sleeping Pizza non ama essere svegliato, quindi ha trasformato {0} e {1} in Calzone Pizza. Rest In Pepperoni. ",
            "{0} è andato per affrontare {1}, ma hanno fatto un meme umido e si sono tolti di mezzo",
            "{0} ha colpito la palla Smash, ma è caduto dal palco prima che potessero usarlo su {1}",
            "{0} ha lanciato una pokeball a {1}, ma era solo un Goldeen"
            ]
        
        self.hugs = [
            "{0} ha dato {1} un imbarazzante abbraccio.",
            "{0} ha finto di dare {1} un abbraccio, ma ha messo un cartello" Kick Me "su di loro.",
            "{0} ha dato {1} un grande abbraccio da orso!",
            "{1}, {0} ti ha appena dato il miglior abbraccio della tua vita!",
            "{0} ha dato {1} un piccolo abbraccio amichevole.",
            "{0} ha cercato di abbracciare {1} ma è stato rifiutato.",
            "{0} tackle-hugs {1}.",
            "{0} ha dato {1} un abbraccio standard da palude",
            "{1} ha segnalato accidentalmente la cosa sbagliata, quindi {0} gli ha dato un abbraccio per smettere {1} di piangere",
            "{0} dà {1} un abbraccio alla zuppa di cereali",
            "{0} si sono abbracciati {1} così forte che sono esplosi in una nuvola di peperoni",
            "{0} va ad abbracciare {1}, che bella amicizia.",
            "{0} abbraccia con successo {1} il potere del Wumpus.",
            "{0} mi ha mandato {1} un po 'di amore, ne ricevo un po' anch'io?",
            "{1} si è abbassato quando {0} ha cercato di abbracciarli.",
            "{0} abbracciato {1} ma {1} lo ha preso come un attacco!",
            "{0} riempie {1} di dolce amore",
            "{0} ha dato {1} un Legacy Hug, in riconoscimento del leggendario Dabbit Prime.",
            "È {0} sicuro di voler abbracciare {1}? Certo, come hanno appena fatto! ',
            "{0} tenta di abbracciarsi {1} ma Dannysaur ha gettato una buccia di banana sul pavimento e {0} è scivolato",
            "{1} è confuso se i cereali sono zuppa o insalata, quindi {0} abbracciati {1} per calmarli"
        ]

     
            
    @commands.command()
    async def fight(self, ctx, user: discord.Member):
        """Lotta contro qualcun'altro per fargli vedere chi comanda!"""
        await ctx.send(random.choice(self.fights).format(ctx.author.name, user.name, ctx.guild.owner.name))


    @commands.command()
    async def hug(self, ctx, user: discord.Member):
        """Abbraccia qualcuno per fargli vedere quanto gli vuoi bene!"""
        await ctx.send(random.choice(self.hugs).format(ctx.author.name, user.name))

        
def setup(bot):
    bot.add_cog(Megadoot(bot))
