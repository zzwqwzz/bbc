from sqlalchemy import create_engine
import pandas as pd
import requests
import json
import os

def de_weight(urls, tempurl, name):
    engine = create_engine('postgresql://postgres:difyai123456@127.0.0.1:5432/agriculture')
    query = "select * from website_article where site_name = '{}'".format(name)
    result = pd.read_sql(query, engine)
    ti = result.loc[-150:, 'url']
    for u in tempurl:
        if len(ti) == 0:
            continue
        else:
            for row in ti:
                if u == row:
                    urls.remove(u)
                    break
                else:
                    continue
    return urls

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
    print(response_out['data']['status'])
    temp = list(response_out['data']['outputs'].values())

    return temp[0]

def Summarize(input_text):
    url = "http://localhost/v1/workflows/run"

    headers = {
        'Authorization': 'Bearer app-bkuEdM9LKj1KpZog6W1gUezJ',
        'Content-Type': 'application/json',
    }

    data = {
        "inputs": {'input': input_text},
        #"response_mode": "streaming",
        "user": "abc-123"
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    response_out = json.loads(response.text)
    print(response_out['data']['status'])
    temp = list(response_out['data']['outputs'].values())

    return temp[0]

def save(name, data, html, title):
    os.makedirs("D:\\desktop\\scrapyspider\\pages\\{}\\{}".format(name, data))
    with open("D:\\desktop\\scrapyspider\\pages\\{}\\{}\\{}.html".format(name, data, title), 'w', encoding='utf-8') as f:
        f.write(html)
        f.close()