from __future__ import unicode_literals

import os
from datetime import datetime

from dateutil.relativedelta import relativedelta
import requests

login_url = 'http://bukkesprangetnatur.barnehage.no/LogOn'
ics_url = ('http://bukkesprangetnatur.barnehage.no/Ukeplan/'
           'PlanMonthAsICalendar/61?year={year}&month={month}')


def main():
    user, password = os.environ['USER'], os.environ['PASSWORD']
    session = requests.Session()
    response = session.post(
        login_url, data={'UserName': user, 'Password': password})
    response.raise_for_status()
    now = datetime.now()
    head = session.get(
        ics_url.format(year=now.year, month=now.month)).text
    tail = session.get(
        ics_url.format(
            year=now.year, month=(
                now + relativedelta(month=1)).month)).text

    # Stitch together the two ics files
    print(('\n'.join(head.split('\n')[:-3])
           + '\n'.join(tail.split('\n')[3:])).encode('utf-8'))
