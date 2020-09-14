import os

from pymongo import MongoClient
from dotenv import load_dotenv

from repositories.member_repo import MemberRepository
from repositories.guild_repo import GuildRepository

from .bot import wwvbot
from .cogs.setup import SetupCog
from .cogs.verification import VerificationCog

def _register_cog(cog):
    wwvbot.add_cog(cog(wwvbot, members_repo, guilds_repo))

load_dotenv()

mongo = MongoClient(
    host=os.getenv('DB_HOSTNAME'),
    port=int(os.getenv('DB_PORT')),
    username=os.getenv('DB_USERNAME'),
    password=os.getenv('DB_PASSWORD')
)

database = mongo[os.getenv('DB_NAME')]

guilds_repo = GuildRepository(database)
members_repo = MemberRepository(database)

wwvbot.add_cog(VerificationCog(wwvbot, os.getenv('BASE_URL'), members_repo, guilds_repo))
_register_cog(SetupCog)

wwvbot.run(os.getenv('DISCORD_TOKEN'))