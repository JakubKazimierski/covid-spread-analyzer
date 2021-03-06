#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

from covid_spread_analyzer.prediction_app.PredictionService import PredictionService

from firebase_admin import credentials, initialize_app

from data_fetch.twitter.DataYieldService import DataYieldService
from covid_spread_analyzer.UpdateService import UpdateService, datetime


def save_log(log_message):
    with open('changelog.md', 'r') as f:
        content = f.read()
        date = datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
        content = content + '\n'
        with open('changelog.md', 'w+') as fw:
            fw.write('## ' + date + '\n' + '- ' +
                     str(log_message) + '\n' + content + '\n')


def main():
    # app setup
    cred = credentials.Certificate('firebase_files/covid-spread-analyzer-firebase-adminsdk-hxchu-8c78edc7cd.json')
    initialize_app(cred, {
        'databaseURL': 'https://covid-spread-analyzer.firebaseio.com/'
    })

    PredictionService.initialize()

    DataYieldService.initialize()
    UpdateService.start()

    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'covid_spread_analyzer.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
