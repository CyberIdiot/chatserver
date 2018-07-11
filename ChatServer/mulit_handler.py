import time
import jpush


# jpush setting
_jpush = jpush.JPush("73232d2b0ba48e696ed64e10", "2bd2574d84ef4986d7ba1c44")
_jpush.set_logging("DEBUG")


def message_handler(json_request):
    # jpush alias
    message = json_request['msg']
    username_from = json_request['name_s']
    username_to = json_request['name_r']
    request_type = 'msg'
    push = _jpush.create_push()
    alias_list = [username_to]
    alias = {"alias": alias_list}
    push.audience = jpush.audience(
        alias
    )
    # push.options = {"time_to_live":86400}
    push.notification = jpush.notification(alert=username_from)
    push.message = jpush.message(message, title=username_from,
                                 extras={"type": request_type, "name_s": username_from, "name_r": username_to})
    push.platform = jpush.all_
    payload = push.send()


def image_handler(json_request):
    file_name = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime()) + ".jpg"
    file_path = "./image/" + file_name
    file_object = open(file_path, "wb+")
    file_object.write(json_request['img'].encode(encoding='ISO-8859-1'))
    file_object.close()
    url = file_path[2:]
    username_from = json_request['name_s']
    username_to = json_request['name_r']
    request_type = 'img'
    push = _jpush.create_push()
    alias_list = [username_to]
    alias = {"alias": alias_list}
    push.audience = jpush.audience(
        alias
    )
    # push.options = {"time_to_live":86400}
    push.notification = jpush.notification(alert=username_from)
    push.message = jpush.message(message=url, title=username_from,
                                 extras={"type": request_type, "name_s": username_from, "name_r": username_to})
    push.platform = jpush.all_
    payload = push.send()


def voice_handler(json_request):
    file_name = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime()) + ".mp3"
    file_path = "./voice/" + file_name
    file_object = open(file_path, "wb+")
    file_object.write(json_request['img'].encode(encoding='ISO-8859-1'))
    file_object.close()
    url = file_path[2:]
    username_from = json_request['name_s']
    username_to = json_request['name_r']
    request_type = 'sou'
    push = _jpush.create_push()
    alias_list = [username_to]
    alias = {"alias": alias_list}
    push.audience = jpush.audience(
        alias
    )
    # push.options = {"time_to_live":86400}
    push.notification = jpush.notification(alert=username_from)
    push.message = jpush.message(message=url, title=username_from,
                                 extras={"type": request_type, "name_s": username_from, "name_r": username_to})
    push.platform = jpush.all_
    payload = push.send()

