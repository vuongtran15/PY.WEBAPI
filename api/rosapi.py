
import http.client
import json

class ROSApi:
    def __init__(self):
        self.base_ip_adress = "172.19.137.206"
        self.base_port = 5204
    
    def conversation_add_message(self, chatid: str, message: str) -> None:
        conn = http.client.HTTPConnection(self.base_ip_adress, self.base_port)
        headers = {'Content-Type': 'application/json'}
        payload = {
            "chatid": chatid,
            "MessageJson": message,
        }
        conn.request("POST", "/api/aichat/server/message/add", json.dumps(payload), headers)
        res = conn.getresponse()
        data = (res.read()).decode("utf-8")
        print(f"Response: {data}")
    
    def conversation_get_command(self, chatid: str):
        conn = http.client.HTTPConnection(self.base_ip_adress, self.base_port)
        conn.request("GET", "/api/aichat/server/message/command?conversationId" + chatid)
        res = conn.getresponse()
        data = (res.read()).decode("utf-8")
        print(f"Response: {data}")
        return data

rosapi = ROSApi()