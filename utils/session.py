class Session:
    current_user = None

    @staticmethod
    def set_user(user):
        Session.current_user = user

    @staticmethod
    def get_user():
        return Session.current_user
