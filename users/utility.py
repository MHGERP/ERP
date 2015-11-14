from django.contrib.auth.models import User
from users.models import UserInfo,Title,Authority

def createNewUser(username, password, fullname = None):
    try:
        user = User.objects.create_user(username = username, password = password)
        user.save()

        userinfo = UserInfo(user = user, name = fullname)
        userinfo.save()
    except IntegrityError, e:
        raise e

def getUserByAuthority(authority):
    auth_obj = Authority.objects.get(authority = authority)
    user_list = User.objects.filter(title_user__authorities = auth_obj)
    return user_list    
