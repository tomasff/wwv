import discord
from discord.ext import commands
from .cog import Cog
from discord.utils import get

class VerificationCog(Cog):
    def __init__(self, bot, base_url, members, guilds):
        super().__init__(bot, members, guilds)

        self.base_url = base_url
    
    @commands.Cog.listener()
    async def on_member_join(self, member):
        record = self._members.find_record_for_member(member)

        if not record:
            return

        if not record['isVerified']:
            return

        guild = member.guild
        role = self._get_guild_role(guild)

        if not role:
            await guild.owner.send('Error in setup found: invalid role id.')
            return

        await member.add_roles(role)

    @commands.command()
    async def verify(self, ctx):
        verify_embed = self._build_base_embed(description='Click on the link below to complete the verification')
        verify_embed.set_thumbnail(url=self.bot.user.avatar_url)

        if not self._members.find_record_for_member(ctx.author):
            record = self._members.add_member(ctx.author)
            verify_embed.add_field(name='Link', value=self._build_verify_link(record.inserted_id))
        else:
            record = self._members.find_record_for_member(ctx.author)
            verify_embed.add_field(name='Link', value=self._build_verify_link(record['_id']))

        verify_embed.add_field(name='Privacy Policy', value=f'For more information on how your information is used `{self.base_url}/privacy`', inline=False)
        await ctx.author.send(embed=verify_embed)

    @commands.command()
    async def check(self, ctx):
        record = self._members.find_record_for_member(ctx.author)

        if not ctx.guild:
            return

        if not record:
            await ctx.channel.send('No verification proccess started! Start by typing wwv!verify')
        else:
            if not record['isVerified']:
                await ctx.author.send('❌ Account not verified. Verify your account by typing wwv!verify')
                return

            role = self._get_guild_role(ctx.guild)

            if not role:
                await ctx.channel.send('Error in setup found: invalid role id. Please contact a member of staff.')
                return

            await ctx.author.send('✅ Account verified and role added')
            await ctx.author.add_roles(role)

    def _build_verify_link(self, id):
        return f'{self.base_url}/redirect/{id}'

    def _build_base_embed(self, description='', title='✅ Verification'):
        embed = discord.Embed(title=title, colour=discord.Colour.from_rgb(91, 48, 105),
                                description=description)

        embed.set_footer(text='This is NOT an offical service from the University of Warwick')
        return embed

    def _get_guild_role(self, guild):
        guild_record = self._guilds.find_record_for_guild(guild)

        if not guild_record:
            return

        roleId = guild_record['verifiedRoleId']
        role = get(guild.roles, id=roleId)

        return role
