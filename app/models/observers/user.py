from app.providers.keys import UserKeys


class UserObserver:
    def creating(self, user):
        user_key = UserKeys()
        user.public_key = user_key.publick_key
        user.private_key = user_key.private_key
