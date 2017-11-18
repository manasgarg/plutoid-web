from bottle import get, post, request, response, run
from blinker import signal as blinker_signal
from plutoid import Executor
import time
import requests
import json
import os
import base64

session_mode = True
ping_interval = 5
input_timeout = 6
max_code_execution_time = 15
code_executor = None

side_effects = []
test_results = []
curr_execution_id = None
curr_input_webhook_url = None

last_activity_time = time.time()


def recv_stdout( sender, content):
    if side_effects and side_effects[-1]['stream'] == 'stdout':
        side_effects[-1] = {'stream': 'stdout', 'content': side_effects[-1]['content'] + content}
    else:
        side_effects.append( {'stream': 'stdout', 'content': content})


def recv_stderr( sender, content):
    side_effects.append( {'stream': 'stderr', 'content': content})


def recv_matplotlib( sender, mimetype, content):
    side_effects.append( {'stream': 'matplotlib', 'mimetype': mimetype, 'content': base64.b64encode( content).decode('utf-8')})


def recv_test_result( sender, content, result):
    test_results.append( {'content': content, 'result': result})


def input_handler( prompt):
    global side_effects

    if not curr_input_webhook_url:
        return ''

    r = requests.post( curr_input_webhook_url, data=json.dumps({'side_effects': side_effects}), timeout=input_timeout)
    side_effects = []

    if r.status_code != 200:
        return ''

    return r.json()['content']


@post('/code-requests/<execution_id>')
def new_code_request( execution_id):
    global side_effects, curr_execution_id, curr_input_webhook_url, last_activity_time, code_executor, test_results

    side_effects = []
    test_results = []
    curr_execution_id = execution_id

    curr_input_webhook_url = request.json.get('input_webhook', None)
    code = request.json['code']
    tests = request.json.get('tests', [])

    has_error = code_executor.exec_code( code, tests)

    last_activity_time = time.time()

    return {'output': side_effects, 'test_results': test_results, 'has_error': has_error}


@get('/keepalive')
def keepalive():
    global last_activity_time 
    last_activity_time = time.time()

    return ''


@post('/inactivity-check')
def inactivity_check():
    global last_activity_time
    if time.time() - last_activity_time > 2*ping_interval:
        os._exit(0)

    return ''

@post('/shutdown')
def shutdown():
    os._exit(0)


def init_kernel(ip_address='0.0.0.0', port=6699, sm=True, pi=5, it=6, mcet=15):
    global session_mode, ping_interval, input_timeout, max_code_execution_time, code_executor
    session_mode = sm
    ping_interval = pi
    input_timeout = it
    max_code_execution_time = mcet

    code_executor = Executor( input_handler, max_code_execution_time)
    run(host=ip_address, port=port)


blinker_signal('plutoid::stdout').connect(recv_stdout)
blinker_signal('plutoid::stderr').connect(recv_stderr)
blinker_signal('plutoid::matplotlib').connect(recv_matplotlib)
blinker_signal('plutoid::test_result').connect(recv_test_result)