import requests
import json

def Translate(input_text):
    url = "http://localhost/v1/workflows/run"

    headers = {
        'Authorization': 'Bearer app-4kfOSVgMHDpvL3w6nZfxvDNf',
        'Content-Type': 'application/json',
    }

    data = {
        "inputs": {'input': input_text},
        #"response_mode": "streaming",
        "user": "abc-123"
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    response_out = json.loads(response.text)
    print(response_out)
    temp = list(response_out['data']['outputs'].values())

    return temp[0]