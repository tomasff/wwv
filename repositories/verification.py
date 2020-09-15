from bson.objectid import ObjectId

class VerificationRepository:
    def __init__(self, database):
        self._verifications = database.verifications

    def start_verification(self, member, guild):
        return self._verifications.insert_one({
            'discordId': member.id,
            'guildId': guild.id
        })

    def find_record_for_member(self, member):
        return self._verifications.find_one({
            'discordId': member.id
        })

    def find_record_for_id(self, id):
        return self._verifications.find_one({
            '_id': ObjectId(id)
        })

    def update_member_verification_guild(self, member, guild):
        return self._verifications.update_one({ 'discordId': member.id }, { '$set': { 'guildId': guild.id } })

    def delete_verification(self, id):
        return self._verifications.remove({ '_id': ObjectId(id) })