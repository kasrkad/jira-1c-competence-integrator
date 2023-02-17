import requests
from os import environ
from logger_config.logger_data import create_logger
from jira_requests.templates.template_requests import GET_ALL_PROJECTS,GET_ALL_TEMPLATES
import json

worker_logger = create_logger(__name__)

try:
    JIRA_HOST = environ["JIRA_HOST"]
    JIRA_AUTH_TOKEN = environ["JIRA_AUTH_TOKEN"]
except Exception:
    worker_logger.critical("Не обнаружена одна из переменных окружения", exc_info=True)


def get_all_jira_project():
    headers = {"Authorization": "Bearer {token}".format(token=JIRA_AUTH_TOKEN),"Accept": "application/json"}
    session = requests.Session()
    try:
        response = session.get(GET_ALL_PROJECTS.format(jira_host=JIRA_HOST), headers=headers)
    except Exception:
        worker_logger.critical(f"Невозможно получить все проекты из jira {JIRA_HOST}", exc_info=True)
        raise

    data = json.loads(response.text)
    result_table = {}
    for elem in data:
        if elem["name"] not in result_table.keys():
            result_table[elem["name"]] = elem["id"]

    return result_table


def get_all_jira_templates():
    headers = {"Authorization": "Bearer {token}".format(token=JIRA_AUTH_TOKEN),"Content-Type": "application/json"}
    session = requests.Session()
    try:
        response = session.get(GET_ALL_TEMPLATES.format(jira_host=JIRA_HOST), headers=headers)
    except Exception:
        worker_logger.critical(f"Невозможно получить все шаблоны из {JIRA_HOST}", exc_info=True)
        raise
    all_templates_json = response.json()
    return all_templates_json


def update_template(template_num):
    pass


def template_loader():
    pass