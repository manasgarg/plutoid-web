from blinker import signal as blinker_signal
import signal
import time
from .logger import log


class CodeExecutionTimeExceeded(Exception):
    pass


last_activity_time = time.time()
execution_start_time = 0
max_code_execution_time = 0
ping_interval = 0


def code_execution_start(sender):
    global execution_start_time
    execution_start_time = time.time()


def code_execution_end(sender):
    global execution_start_time, last_activity_time
    execution_start_time = 0
    last_activity_time = time.time()


def keep_alive(sender):
    global last_activity_time
    last_activity_time = time.time()


def sigalrm_handler(signum, frame):
    log('monitor', {'type': 'monitor_wakeup'})

    curr_time = time.time()

    if execution_start_time and curr_time - execution_start_time > max_code_execution_time:
        log('monitor', {'type': 'code_exec_timeout'})
        raise CodeExecutionTimeExceeded()
    elif curr_time - last_activity_time > 2*ping_interval:
        log('monitor', {'type': 'keep_alive_timeout'})
        import os
        os._exit(0)
    else:
        signal.alarm(5)


def init_monitor(max_exec_time=15, ping=15):
    global max_code_execution_time, ping_interval
    max_code_execution_time = max_exec_time
    ping_interval = ping

    blinker_signal('plutoid::code_execution_start').connect(code_execution_start)
    blinker_signal('plutoid::code_execution_end').connect(code_execution_end)
    blinker_signal('plutoidweb::keep_alive').connect(keep_alive)

    signal.signal(signal.SIGALRM, sigalrm_handler)
    signal.alarm(5)