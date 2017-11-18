#!/usr/bin/env python3

import click
import logging
import logging.config
from plutoid_web.kernel import init_kernel

logger = logging.getLogger(__name__)


def setup_logging(verbose, logdir):
    loglevel = logging.INFO
    if verbose: loglevel = logging.DEBUG

    logging.config.dictConfig({
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
            },
        },
        'handlers': {
            'default': {
                'level': loglevel,
                'class': 'logging.StreamHandler',
                'formatter': 'standard'
            },
        },
        'loggers': {
            '': {
                'handlers': ['default'],
                'level': loglevel,
                'propagate': True
            }
        }
    })


@click.command()
@click.option('--ip-address', default='0.0.0.0')
@click.option('--port', default=6699)
@click.option('--verbose', is_flag=True)
@click.option('--logdir')
@click.option('--session-mode', is_flag=True)
@click.option('--ping-interval', default=15)
@click.option('--input-timeout', default=60)
@click.option('--max-code-execution-time', default=15)
def main( ip_address, port, verbose, logdir, session_mode, ping_interval, input_timeout, max_code_execution_time):
    setup_logging(verbose, logdir)

    logger.info('Starting plutoid kernel...')

    init_kernel(ip_address, port, session_mode, ping_interval, input_timeout, max_code_execution_time)


if __name__ == "__main__":
    main()