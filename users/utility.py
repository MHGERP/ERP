from django.contrib.auth.models import User
from users.models import UserInfo

def createNewUser(username, password, fullname = None):
    try:
        user = User(username = username, password = password)
        user.save()

        userinfo = UserInfo(user = user, name = fullname)
        userinfo.save()
    except IntegrityError, e:
        raise e
