from ._base import BaseView
from momeet.models.user import User


class GetAuthToken(BaseView):
    def get(self):
        return User.generate_auth_token()


