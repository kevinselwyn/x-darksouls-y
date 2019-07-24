#!/usr/bin/env python
# coding=utf-8
# pylint: disable=C0103,C0301
"""X is the Dark Souls of Y server"""

import argparse
import os
import _thread
import requests
import x_darksouls_y
from flask import Flask
from apscheduler.schedulers.blocking import BlockingScheduler

app = Flask(__name__)

@app.route('/')
def root():
    """Root route"""

    return 'OK'

def main():
    """Main function"""

    parser = argparse.ArgumentParser()

    parser.add_argument('--consumer-key', type=str, dest='consumer_key', default=None, required=(False if os.getenv('CONSUMER_KEY', None) else True))
    parser.add_argument('--consumer-secret', type=str, dest='consumer_secret', default=None, required=(False if os.getenv('CONSUMER_SECRET', None) else True))
    parser.add_argument('--access-token-key', type=str, dest='access_token_key', default=None, required=(False if os.getenv('ACCESS_TOKEN_KEY', None) else True))
    parser.add_argument('--access-token-secret', type=str, dest='access_token_secret', default=None, required=(False if os.getenv('ACCESS_TOKEN_SECRET', None) else True))
    parser.add_argument('--pattern', type=str, dest='pattern', default=None, required=False)
    parser.add_argument('--search', type=str, dest='search_term', default=None, required=False)

    parser.add_argument('--url', type=str, dest='url', default='http://0.0.0.0:8000', required=(False if os.getenv('URL', None) else True))
    parser.add_argument('--host', type=str, dest='host', default='0.0.0.0', required=False)
    parser.add_argument('--port', type=int, dest='port', default=8000, required=False)

    args = parser.parse_args()

    def run_flask():
        """Run server"""

        app.run(host=args.host, port=args.port)

    def run_awake():
        """Run awake"""

        url = os.getenv('URL', args.url)
        _r = requests.get(url)

    def run_job():
        """Run job"""

        x_darksouls_y.run(args)

    scheduler = BlockingScheduler()
    scheduler.add_job(run_job, 'cron', minute='0,30')
    scheduler.add_job(run_awake, 'cron', minute='5,25,45')
    print('Press Ctrl+%s to exit' % ('Break' if os.name == 'nt' else 'C'))

    try:
        _thread.start_new_thread(run_flask, ())
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()

if __name__ == '__main__':
    main()
