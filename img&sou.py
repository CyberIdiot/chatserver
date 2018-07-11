json_request = json.loads(request.body.decode())
        foo=open("1.aac","wb+");
        foo.write(json_request['file'].encode(encoding='ISO-8859-1'))
        foo.close()
        print(json_request['file'].encode(encoding='ISO-8859-1'))