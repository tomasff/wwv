import discord
from discord.ext import commands, tasks
from .cog import Cog
from discord.utils import get
from ..utils.embeds import build_verify_embed, LOADING, ACCOUNT_VERIFIED

class VerificationCog(Cog):
    def __init__(self, bot, base_url, pubsub, verifications, members, guilds):
        super().__init__(bot, members, guilds)

        self._verifics = verifications
        self._pubsub = pubsub
        self._base_url = base_url

        self.assign_role_on_verification.start()

    def cog_unload(self):
        self._pubsub.unsubscribe()
        self.assign_role_on_verification.cancel()

    @tasks.loop(seconds=1)
    async def assign_role_on_verification(self):
        message = self._pubsub.get_message()

        if not message:
            return
        
        if message['type'] != 'message':
            return

        data = message['data'].decode('utf-8') 
        discord_id, guild_id = data.split(',')

        guild = self.bot.get_guild(int(guild_id))
        user = guild.get_member(int(discord_id))

        success = self._add_verified_role(ctx.author, ctx.guild)

        if not success:
            await user.send('Error in setup found: invalid role id. Please contact a member of staff.')
        else:
            await user.send(embed=ACCOUNT_VERIFIED)
    
    @commands.Cog.listener()
    async def on_member_join(self, member):
        record = self._members.find_record_for_member(member)

        if not record:
            return

        guild = member.guild
        role = self._get_guild_role(guild)

        if not role:
            await guild.owner.send('Error in setup found: invalid role id.')
            return

        await member.add_roles(role)

    @commands.command()
    async def verify(self, ctx):
        member_record = self._members.find_record_for_member(ctx.author)

        if member_record:
            await ctx.author.send('✅ Your Discord account is already verified!')
            return

        verif_record = self._verifics.find_record_for_member(ctx.author)

        if not verif_record:
            verif_id = self._verifics.start_verification(ctx.author, ctx.guild).inserted_id
        else:
            verif_id = verif_record['_id']

            if verif_record['guildId'] != ctx.guild:
                self._verifics.update_member_verification_guild(ctx.author, ctx.guild)

        verify_embed = build_verify_embed(self.bot.user.avatar_url, self._build_verify_link(verif_id))

        await ctx.author.send(embed=verify_embed)
        await ctx.author.send(embed=LOADING)

    @commands.command()
    async def check(self, ctx):
        record = self._members.find_record_for_member(ctx.author)

        if not ctx.guild:
            return

        if not record:
            await ctx.channel.send('❌ Account not verified. Verify your account by typing wwv!verify')
        else:
            success = self._add_verified_role(ctx.author, ctx.guild)

            if success:
                await ctx.author.send(embed=ACCOUNT_VERIFIED)
            else:
                await ctx.channel.send('Error in setup found: invalid role id. Please contact a member of staff.')

    def _build_verify_link(self, id):
        return f'{self._base_url}/redirect/{id}'

    def _get_guild_role(self, guild):
        guild_record = self._guilds.find_record_for_guild(guild)

        if not guild_record:
            return

        roleId = guild_record['verifiedRoleId']
        role = get(guild.roles, id=roleId)

        return role

    async def _add_verified_role(self, member, guild):
        role = self._get_guild_role(ctx.guild)

        if not role:
            return False

        await ctx.author.add_roles(role)
        return True