import utils

import json
import yaml
import requests

config = {}
user_info = {}

def get_login_post_body(username: str, password: str):
    password_hashed = utils.md5_encrypt(password)
    ut = utils.get_login_string(username, password_hashed)

    hash_map = {
        'loginName': username,
        'password': password_hashed,
        'ut': ut,
        'device': config['logininfo']['device'],
        'appVersion': config['logininfo']['appVersion'],
        'webEnv': config['logininfo']['webEnv'],
        'registrationId': config['logininfo']['registrationId']
    }
    
    json_payload = json.dumps(hash_map, separators = (',', ':'))
    y = utils.get_c_str(json_payload)

    post_body = json.dumps({
        'y': y
    }, separators = (',', ':'))
    return post_body

def login():
    login_post_body = get_login_post_body(config['username'], config['password'])
    login_resp = requests.post('https://apps.ulearning.cn/login/v2',
        data = login_post_body, 
        headers = {
            'User-Agent': config['UA'],
            'Content-Type': 'application/json',
            'uversion': '2'
        }
    )

    login_result = login_resp.json()['result']
    return utils.decode_result(login_result)

def get_course_list():
    resp = requests.get('https://courseapi.ulearning.cn/courses/students?publishStatus=1&pn=1&ps=20&type=1',
        headers = {
            'User-Agent': config['UA'],
            'Authorization': user_info['token']
        }
    )
    resp_json = resp.json()
    return resp_json['courseList']

with open('config.yaml') as f:
    config = yaml.safe_load(f)

user_info = login()
course_list = get_course_list()