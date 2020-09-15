class GuildRepository:
    def __init__(self, database):
        self._guilds = database.guilds

    def add_guild(self, guild, verified_role):
        return self._guilds.insert_one({
            'guildId': guild.id,
            'verifiedRoleId': verified_role.id,
        })

    def find_record_for_guild(self, guild):
        return self._guilds.find_one({
            'guildId': guild.id
        })

    def update_guild(self, guild, verified_role):
        return self._guilds.update_one({ 'guildId': guild.id }, {
            '$set': {
                'verifiedRoleId': verified_role.id,
            }
        })

    def remove_guild(self, guild):
        return self._guilds.remove({ 'guildId': guild.id })