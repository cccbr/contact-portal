"""Jira Connection
:author: Martyn B
"""
import os
from atlassian.jira import Jira as _Jira
from dotenv import dotenv_values

env = os.environ.get('ENV', None)
if env == "PROD":
    ENV = "portal/.env"
elif env == "DEV":
    ENV = "portal/.env.fake"
else:
    raise RuntimeError('Provide an ENV=DEV|PROD')


def get_jira_client():
    """ Get Jira Client
    """
    conf = dotenv_values(ENV)
    try:
        url = conf["JIRA_URL"]
    except KeyError:
        return None
    try:
        user = conf["JIRA_USERNAME"]
    except KeyError:
        return None
    try:
        passwd = conf["JIRA_PASSWORD"]
    except KeyError:
        return None
    return _Jira(url=url, username=user, password=passwd, cloud=True)
