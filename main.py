import utils

import json
import yaml
import requests
import time
import os

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

    try:
        login_resp = requests.post('https://apps.ulearning.cn/login/v2',
            data = login_post_body, 
            headers = {
                'User-Agent': config['UA'],
                'Content-Type': 'application/json',
                'uversion': '2'
            }
        )
        resp_json = login_resp.json()
        login_result = resp_json['result']
        return utils.decode_result(login_result)
    except Exception as e:
        print(f'登录时发生错误：{e}')
        exit(0)

def get_course_list():
    try:
        resp = requests.get('https://courseapi.ulearning.cn/courses/students?publishStatus=1&pn=1&ps=20&type=1',
            headers = {
                'User-Agent': config['UA'],
                'Authorization': user_info['token']
            }
        )
        resp_json = resp.json()
        return resp_json['courseList']
    except Exception as e:
        print(f'获取课程列表时发生错误：{e}')
        return []

def get_activity_list(courseID: int):
    try:
        resp = requests.get(f'https://courseapi.ulearning.cn/appHomeActivity/v4/{courseID}',
            headers = {
                'User-Agent': config['UA'],
                'Authorization': user_info['token']
            }
        )
        resp_json = resp.json()
        return resp_json['otherActivityDTOList']
    except Exception as e:
        print(f'获取课堂活动时发生错误：{e}')
        return []

def checkin_by_location(attendanceID: int, classID: int):
    data = json.dumps({
        'attendanceID': attendanceID,
        'classID': classID,
        'userID': user_info['userID'],
        'location': config['location'],
        'address': config['address'],
        'enterWay': '1',
        'attendanceCode': ''
    }, separators = (',', ':'))

    try:
        resp = requests.post('https://apps.ulearning.cn/newAttendance/signByStu',
            data = data,
            headers = {
                'User-Agent': config['UA'],
                'Authorization': user_info['token'],
                'Content-Type': 'application/json'
            }
        )
        resp_json = resp.json()
        if resp_json['status'] == 200:
            print('签到成功')
        else:
            print(f'签到失败：{resp_json["message"]}')
    except Exception as e:
        print(f'签到时发生错误：{e}')

def check_activity(course_list):
    flag = False
    for course in course_list:
        activity_list = get_activity_list(course['id'])
        for activity in activity_list:
            if activity['status'] == 2 and activity['personStatus'] == 0:
                print(f"课程 {course['name']} 正在进行 {activity['title']}")
                checkin_by_location(activity['relationId'], course['classId'])
                flag = True
    if flag == False:
        print('暂无签到')

if not os.path.exists('config.yaml'):
    print('config.yaml 不存在')
    exit(0)
else:
    with open('config.yaml') as f:
        config = yaml.safe_load(f)

user_info = login()
course_list = get_course_list()

while True:
    check_activity(course_list)
    time.sleep(config['interval'] / 1000)