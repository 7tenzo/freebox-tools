#!/usr/bin/python3

import hmac
import time
import os
from apize.apize import Apize

api_url="http://192.168.1.254/api/v8"
app = Apize('http://192.168.1.254/api/v8')
CONST_APP_TOKEN="XXXXXXXXXXXXXXXXX"


@app.call('/login/session/', method='POST')
def connect_app(app_token, app_id, challenge):
	h = hmac.new(app_token.encode(), challenge, 'sha1')
	password = h.hexdigest()

	data = {'app_id': app_id, 'password': password}
	headers = {'X-Fbx-App-Auth': app_token}

	return {
		'data': data,
		'headers': headers,
		'is_json': True
	}


@app.call('/system/reboot/', method='POST')
def call_reboot(session_token):
	headers = {'X-Fbx-App-Auth': session_token}
	return {'headers': headers}


@app.call('/login/authorize/:id')
def authorize_app(track_id):
	args = {'id': track_id}

	return {'args': args}


def get_session_token(app_token, app_id, track_id):
	response = authorize_app(track_id)
	challenge = response['data']['result']['challenge'].encode()
	conn = connect_app(app_token, app_id, challenge)
	session_token = conn['data']['result']['session_token']
	return session_token


if __name__ == '__main__':
	app_token = CONST_APP_TOKEN
	app_id = 'fr.freebox.reboot'
	track_id = 0
	session_token = get_session_token(app_token, app_id, track_id)
	if session_token:
		#print(session_token)
		call_reboot(session_token)
		time.sleep(10)
		exit()
