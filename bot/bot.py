import discord
from discord.ext import commands

import redis
from pymongo import MongoClient

from repositories.member import MemberRepository
from repositories.guild import GuildRepository
from repositories.verification import VerificationRepository

from .cogs.setup import SetupCog
from .cogs.verification import VerificationCog

from .config import Config

intents = discord.Intents.default()
intents.members = True

description = 'Verify your affiliation with the University of Warwick using your ITS account'
wwvbot = commands.Bot(command_prefix='wwv!', description=description, intents=intents)

mongo = MongoClient(
    host=Config.DB_HOSTNAME,
    port=Config.DB_PORT,
    username=Config.DB_USERNAME,
    password=Config.DB_PASSWORD
)

database = mongo[Config.DB_NAME]

r = redis.Redis(host=Config.REDIS_HOSTNAME, port=Config.REDIS_PORT, db=0)

pubsub = r.pubsub()
pubsub.subscribe(Config.REDIS_PUBSUB_CH)

guilds_repo = GuildRepository(database)
members_repo = MemberRepository(database)
verif_repo = VerificationRepository(database)

wwvbot.add_cog(VerificationCog(wwvbot, Config.BASE_URL, pubsub, verif_repo, members_repo, guilds_repo))
wwvbot.add_cog(SetupCog(wwvbot, members_repo, guilds_repo))