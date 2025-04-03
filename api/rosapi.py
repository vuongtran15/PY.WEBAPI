
import http.client
import json
import ssl

class ROSApi:
    def __init__(self):
        self.base_ip_adress = "172.19.137.206"
        self.base_port = 5204
    
    def conversation_add_message(self, chatid: str, message: str) -> None:
        conn = http.client.HTTPSConnection(self.base_ip_adress, self.base_port, context=ssl._create_unverified_context())
        headers = {'Content-Type': 'application/json'}
        payload = {
            "chatid": chatid,
            "MessageJson": message,
        }
        conn.request("POST", "/api/aichat/server/message/add", json.dumps(payload), headers)
        res = conn.getresponse()
        data = (res.read()).decode("utf-8")
    
    def conversation_get_command(self, chatid: str):
        conn = http.client.HTTPSConnection(self.base_ip_adress, self.base_port, context=ssl._create_unverified_context())
        conn.request("GET", "/api/aichat/server/message/command?conversationId=" + chatid)
        res = conn.getresponse()
        data = (res.read()).decode("utf-8")
        return data
    
    def conversation_get_prompt(self, chatid: str):
        conn = http.client.HTTPSConnection(self.base_ip_adress, self.base_port, context=ssl._create_unverified_context())
        conn.request("GET", "/api/aichat/server/message/prompt?conversationId=" + chatid)
        res = conn.getresponse()
        data = (res.read()).decode("utf-8")
        return data

rosapi = ROSApi()