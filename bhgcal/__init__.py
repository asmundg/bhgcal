from __future__ import unicode_literals

from datetime import datetime
import os
import sys

from dateutil.relativedelta import relativedelta
import requests

bases = {'r\xf8sslyngen': 59,
         'myrulla': 61}

login_url = 'http://bukkesprangetnatur.barnehage.no/LogOn'
ics_url = ('http://bukkesprangetnatur.barnehage.no/Ukeplan/'
           'PlanMonthAsICalendar/{base}?year={year}&month={month}')


def stdin_decode(data):
    if sys.stdin.encoding is not None:
        return data.decode(sys.stdin.encoding)
    else:
        # Just assume we're modern if nothing else is specified
        return data.decode('utf-8')


def stdout_encode(data):
    if sys.stdout.encoding is not None:
        return data.encode(sys.stdout.encoding)
    else:
        # Just assume we're modern if nothing else is specified
        return data.encode('utf-8')


def main():
    base, user, password = (
        stdin_decode(os.environ['BASE']), os.environ['USER'],
        os.environ['PASSWORD'])
    session = requests.Session()
    response = session.post(
        login_url, data={'UserName': user, 'Password': password})
    response.raise_for_status()
    now = datetime.now()
    next = now + relativedelta(month=1)
    head = (
        session.get(ics_url.format(
            base=bases[base], year=now.year, month=now.month))
        .content.decode('utf-8'))
    tail = (
        session.get(
            ics_url.format(
                base=bases[base], year=next.year, month=next.month))
        .content.decode('utf-8'))

    # Stitch together the two ics files
    print(stdout_encode('\n'.join(head.split('\n')[:-3])
                        + '\n'.join(tail.split('\n')[3:])))
