from django.shortcuts import render
from django.http import HttpResponse
from ChatServer.models import AppUser, UserProfile
from ChatServer.mulit_handler import message_handler, image_handler, voice_handler
from django.core.exceptions import ObjectDoesNotExist
from os import makedirs
import json
import jpush

# Jpush setting

_jpush = jpush.JPush("05b80105b6611b3e650ea234", "5e904c7030772f14a31fd382")
_jpush.set_logging("DEBUG")

# Create your views here.


def user_login(request):
    if request.method == 'POST':
        json_request = json.loads(request.body.decode())
        request_type = json_request['type']
        if request_type == '0':
            username = json_request['name']
            password = json_request['password']
            user = AppUser.objects.get(UserName=username)
            if user is not None or user.Active != 'No':
                return 404
                # some one had logged in this account
            if user.Password == password:
                user.Active = 'Yes'
                user.save()
                json_response = {"type": "0", "name": username}
                return json_response
    return 404


def user_signup(request):
    if request.method == 'POST':
        json_request = json.loads(request.body.decode())
        # print(request.body)
        request_type = json_request['type']
        # print(type(request_type))
        if request_type == '1':
            username = json_request['name']
            password = json_request['password']
            nickname = json_request['nickname']
            email = json_request['email']
            birthday = json_request['birthday']
            avatar = json_request['avatar']
            # try:
           # user = AppUser.objects.filter(UserName=username)
               # user_profile = UserProfile.objects.filter(LinkUser=user)
                # A user using the same user name exist
               # return 200
           # except ObjectDoesNotExist:
           # if user is None:
            user = AppUser(UserName=username, Password=password, Email=email)
            user.save()
            user_profile = UserProfile(LinkUser=user, NickName=nickname, Birthday=birthday, Avatar=avatar)
            user_profile.save()
            json_response = {"type": "1", "name": username}
            print(json_response)
            return json_response
    return 404


def friend_list_request(request):
    if request.method == 'POST':
        json_request = json.loads(request.body.decode())
        request_type = json_request['type']
        if request_type == '2':
            username = json_request['name']
            user = AppUser.objects.get(UserName=username)
            if user is None or user.Active != 'Yes':
                return 404
            user_profile = user.userprofile
            friend_list = user_profile.Friends
            if friend_list is None:
                json_response = {"type": "2","name": "null","nickname":"null"}
                return json_response
            else:
                friend_name_list = []
                friend_nick_list = []
                json_response = {"type":"2", "name":friend_name_list, "nickname":friend_nick_list}
                for select_friend in friend_list.all():
                    if select_friend is None:
                        break
                    friend_name = select_friend.LinkUser.UserName
                    friend_nick = select_friend.NickName
                    json_response['name'].append(friend_name)
                    json_response['nickname'].append(friend_nick)
                return json_response
    return 404


def profile_request(request):
    if request.method == 'POST':
        json_request = json.loads(request.body.decode())
        request_type = json_request['type']
        if request_type == '3':
            username = json_request['name']
            user = AppUser.objects.get(UserName=username)
            if user is None:
                return 404
            user_profile = user.userprofile
            if user_profile is None:
                return 404
            nickname = user_profile.NickName
            email = user.Email
            birthday = user_profile.Birthday
            avatar = user_profile.Avatar
            # birthday = str(birthday)
            json_response = {"type": "3", "nickname": nickname, "email": email, "birthday": birthday, "avatar": avatar}
            return json_response
    return 404


def profile_update(request):
    if request.method == 'POST':
        json_request = json.loads(request.body.decode())
        request_type = json_request['type']
        if request_type == '4':
            username = json_request['name']
            user = AppUser.objects.get(UserName=username)
            if user is None or user.Active == 'No':
                return 404
            user_profile = user.userprofile
            if user_profile is None:
                return 404
            password = json_request['password']
            nickname = json_request['nickname']
            email = json_request['email']
            birthday = json_request['birthday']
            avatar = json_request['avatar']
            user_profile.NickName = nickname
            user_profile.Avatar = avatar
            user_profile.save()
            user.Password = password
            user.Email = email
            user.Birthday = birthday
            # change birthday failed, why?
            user.save()
            json_response = {"type": "4"}
            return json_response
    return 404


def send_message(request):
    if request.method == 'POST':
        json_request = json.loads(request.body.decode())
        request_type = json_request['type']
        if request_type == '5':
            username_from = json_request['name_s']
            user_from = AppUser.objects.get(UserName=username_from)
            if user_from is None or user_from.Active != 'Yes':
                return 404
            username_to = json_request['name_r']
            user_to = AppUser.objects.get(UserName=username_to)
            if user_to is None:
                return 404
            message = json_request['msg']
            if message == 'None':
                img = json_request['img']
                if img == 'None':
                    voice = json_request['sou']
                    if voice == 'None':
                        return 404
                    else:
                        voice_handler(json_request)
                else:
                    image_handler(json_request)
            else:
                message_handler(json_request)
            json_response = {"type": "5","name_s": username_from, "name_r": username_to}
            return json_response
    return 404


def friend_add(request):
    if request.method == 'POST':
        json_request = json.loads(request.body.decode())
        request_type = json_request['type']
        if request_type == '6':
            username_from = json_request['name_s']
            user_from = AppUser.objects.get(UserName=username_from)
            if user_from is None or user_from.Active != 'Yes':
                return 404
            username_to = json_request['name_r']
            user_to = AppUser.objects.get(UserName=username_to)
            if user_to is None:
                return 404
            user_from_profile = user_from.userprofile
            user_to_profile = user_to.userprofile
            user_from_profile.Friends.add(user_to_profile)
            user_to_profile.Friends.add(user_from_profile)

            # jpush message

            message = "Added you"
            push = _jpush.create_push()
            alias_list = [username_to]
            alias = {"alias": alias_list}
            push.audience = jpush.audience(
                alias
            )
            # push.options = {"time_to_live":86400}
            push.notification = jpush.notification(alert=username_from)
            push.message = jpush.message(message, title=username_from,
                                         extras={"name_s": username_from, "name_r": username_to})
            push.platform = jpush.all_
            push.send()

            # jpush message sent

            json_response = {"type": "6"}
            return json_response
    return 404


def user_logout(request):
    if request.method == 'POST':
        json_request = json.loads(request.body.decode())
        request_type = json_request['type']
        if request_type == 'user_logout':
            username = json_request['name']
            user = AppUser.objects.get(UserName=username)
            if user is None or user.Active != 'Yes':
                return 404
            user.Active = 'No'
            json_response = {"type": "user_logout", "name": username}
            return json_response
    return 404


def friend_del(request):
    if request.method == 'POST':
        json_request = json.loads(request.body.decode())
        request_type = json_request['type']
        if request_type == '7':
            username_from = json_request['name_s']
            user_from = AppUser.objects.get(UserName=username_from)
            if user_from is None or user_from.Active != 'Yes':
                return 404
            username_to = json_request['name_r']
            user_to = AppUser.objects.get(UserName=username_to)
            if user_to is None:
                return 404
            user_from_profile = user_from.userprofile
            user_to_profile = user_to.userprofile
            user_from_profile.Friends.remove(user_to_profile)
            user_from_profile.save()

            #jpush message

            if request_type == "7":
                message = "Removed you"
            if request_type == 'add_delete':
                message = "Reject you"
            push = _jpush.create_push()
            alias_list = [username_to]
            alias = {"alias": alias_list}
            push.audience = jpush.audience(
                alias
            )
            # push.options = {"time_to_live":86400}
            push.notification = jpush.notification(alert=username_from)
            push.message = jpush.message(message, title=username_from,
                                         extras={"name_s": username_from, "name_r": username_to})
            push.platform = jpush.all_
            push.send()

            #jpush message sent

            json_response = {"type": "7"}
            return json_response
    return 404


def image_response(request, file_name):
    if request.method == 'POST':
        file_object = open("./image/" + file_name, "rb+")
        # json_response = {"type":"img", "contain": file_object.read()}
        # return json_response
        return HttpResponse(content=file_object.read(),
                            status=200,
                            content_type="image/jpeg")
    return HttpResponse(content=b'', status=404, )


def voice_response(request, file_name):
    if request.method == 'POST':
        file_object = open("./voice/" + file_name, "rb+")
        # json_response = {"type":"sou", "contain": file_object.read()}
        # return json_response
        return HttpResponse(content=file_object.read(),
                            status=200,
                            content_type="audio/mp3")
        HttpResponse(content=b'', status=404, )




