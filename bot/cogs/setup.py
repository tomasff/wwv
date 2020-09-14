from discord import Role
from discord.ext import commands
from discord.utils import get
from .cog import Cog

class SetupCog(Cog):
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        await guild.owner.send('Thank you for adding WW Verify!')
        await guild.owner.send('Please setup the verified role ID with `wwv!setup <verified user role>`')

    @commands.Cog.listener()
    async def on_guild_leave(self, guild):
        self._guilds.remove_guild(guild)

    @commands.command()
    async def setup(self, ctx, verified_role: Role):
        if not ctx.guild:
            await ctx.author.send('This command must be executed inside a guild!')
            return
        
        if ctx.guild.owner != ctx.author:
            await ctx.author.send('This command can only be used by the guild owner!')
            return

        record = self._guilds.find_record_for_guild(ctx.guild)

        if record:
            self._guilds.update_guild(ctx.guild, verified_role)
        else:
            self._guilds.add_guild(ctx.guild, verified_role)
        
        await ctx.channel.send('Server setup successfully!')
        await ctx.channel.send('Details can be updated using the same command i.e. `wwv!setup <verified user role>`')