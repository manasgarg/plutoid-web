#!/usr/bin/env python3

import click
import logging
import logging.config
from ..kernel import init_kernel
from ..logger import init_logger

@click.command()
@click.option('--ip-address', default='0.0.0.0')
@click.option('--port', default=6699)
@click.option('--session-mode', is_flag=True)
@click.option('--ping-interval', default=15)
@click.option('--input-timeout', default=60)
@click.option('--max-code-execution-time', default=15)
def main( ip_address, port, session_mode, ping_interval, input_timeout, max_code_execution_time):
    init_logger('plutoidweb-{}'.format(port))
    init_kernel(ip_address, port, session_mode, ping_interval, input_timeout, max_code_execution_time)


if __name__ == "__main__":
    main()