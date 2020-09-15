from bson.objectid import ObjectId

class VerificationRepository:
    def __init__(self, database):
        self._verifications = database.verifications

    def start_verification(self, member, guild):
        return self._verifications.insert_one({
            'discordId': member.id,
            'guildId': guild.id
        })

    def delete_verification(self, id):
        return self._verifications.remove({ '_id': ObjectId(id) })