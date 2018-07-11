from django.http import HttpRequest, HttpResponse
from ChatServer.views import user_login, user_signup, friend_list_request, profile_request, profile_update, send_message, friend_add, user_logout, friend_del
import json

# deal with requests from our app


def json_handler(request):
    if request.method == 'POST':
        print(request.body)
        json_request = json.loads(request.body.decode())
        print(json_request)
        request_type = json_request['type']
        print(type(request_type))
        if request_type == '0':
            json_response = user_login(request)
        elif request_type == '1':
            json_response = user_signup(request)
        elif request_type == '2':
            json_response = friend_list_request(request)
        elif request_type == '3':
            json_response = profile_request(request)
        elif request_type == '4':
            json_response = profile_update(request)
        elif request_type == '5':
            json_response = send_message(request)
        elif request_type == '6':
            json_response = friend_add(request)
        elif request_type == 'user_logout':
            json_response = user_logout(request)
        elif request_type == '7' or request_type == "add_delete":
            json_response = friend_del(request)
        if json_response == 404:
            return HttpResponse(content=b'', status=404, )
        elif json_response == 200:
            return HttpResponse(content=b'', status=200, )
        else:
            return HttpResponse(content=json.dumps(json_response, ensure_ascii=False),
                                status=200,
                                content_type="application/json")
    else:
        return HttpResponse(content=b'', status=404, )