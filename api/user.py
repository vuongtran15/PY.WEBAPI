import json
import fastapi
from fastapi import HTTPException
from pydantic import BaseModel
import http.client

router = fastapi.APIRouter()

class LoginRequest(BaseModel):
    username: str
    password: str

@router.post("/login")
async def login_ros(request: LoginRequest):
    print("Login GET endpoint called + username: " + request.username + " password: " + request.password)
    conn = http.client.HTTPSConnection("ros.reginamiracle.com", 8109)
    payload = ''
    headers = {}
    conn.request("POST", "/common/login?username=" + request.username + "&password=" + request.password, payload, headers)
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))
    code_status = res.status



    if code_status == 200:
        # return convert data to json
        json_data = data.decode("utf-8")
        json_data = json.loads(json_data)
        # create a token from jwt for json_data
        json_data["token"] = "Bearer " + json_data["token"]
        return json_data
    else:
        raise HTTPException(status_code=code_status, detail="Login failed")


