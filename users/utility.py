from django.contrib.auth.models import User
from users.models import UserInfo

def createNewUser(username, password):
    try:
        user = User(username = username, password = password)
        user.save()

        userinfo = UserInfo(user = user)
        userinfo.save()
    except IntegrityError, e:
        raise e
