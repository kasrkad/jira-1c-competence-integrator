from os import environ
import json
import requests
from logger_config.logger_data import create_logger
from jira_requests.templates.template_requests import GET_ALL_PROJECTS, TEMPLATE_ENDPOINT, TEMPLATE_ID_ENDPOINT

worker_logger = create_logger(__name__)

try:
    JIRA_HOST = environ["JIRA_HOST"]
    JIRA_AUTH_TOKEN = environ["JIRA_AUTH_TOKEN"]
except Exception:
    worker_logger.critical(
        "Не обнаружена одна из переменных окружения", exc_info=True)
    exit()


def jira_get_all_projects() -> dict:
    headers = {"Authorization": "Bearer {token}".format(
        token=JIRA_AUTH_TOKEN), "Accept": "application/json"}
    session = requests.Session()
    try:
        response = session.get(GET_ALL_PROJECTS.format(
            jira_host=JIRA_HOST), headers=headers)
        if not response.ok:
            raise ValueError(
                f"При получении всех проектов для извлечения id произошла ошибка, код ответа {response.status_code}")
    except Exception:
        worker_logger.critical(
            f"Невозможно получить все проекты из jira {JIRA_HOST}", exc_info=True)
        raise

    data = json.loads(response.text)
    result_table = {}
    for elem in data:
        if elem["name"] not in result_table:
            result_table[elem["name"]] = elem["id"]

    return result_table


def jira_get_all_templates() -> dict:
    headers = {"Authorization": "Bearer {token}".format(
        token=JIRA_AUTH_TOKEN), "Content-Type": "application/json"}
    session = requests.Session()
    try:
        response = session.get(TEMPLATE_ENDPOINT.format(
            jira_host=JIRA_HOST), headers=headers)
        if not response.ok:
            raise ValueError(
                f"Проблема при запросе всех шаблонов из {JIRA_HOST}, код ответа {response.status_code}")
    except Exception:
        worker_logger.error(
            f"Невозможно получить все шаблоны из {JIRA_HOST}", exc_info=True)
        raise
    all_templates_json = response.json()
    return all_templates_json


def update_template(template_num):
    pass


def template_loader(template_data: list) -> None:
    headers = {"Authorization": "Bearer {token}".format(
        token=JIRA_AUTH_TOKEN), "Content-Type": "application/json"}
    session = requests.Session()
    for template in template_data:
        try:
            response = session.post(TEMPLATE_ENDPOINT.format(jira_host=JIRA_HOST),
                                    headers=headers, data=json.dumps(template))
            if not response.ok:
                raise ValueError(
                    f'Проблема при создании шаблона код ответа {response.status_code} текст ошибки {response.text}')
        except Exception:
            worker_logger.error(
                f'При загрузке шаблона {template} произошла ошибка', exc_info=True)
    return None


def delete_template(template_id):
    headers = {"Authorization": "Bearer {token}".format(
        token=JIRA_AUTH_TOKEN)}
    session = requests.Session()
    try:
        response = session.delete(TEMPLATE_ID_ENDPOINT.format(
            jira_host=JIRA_HOST, template_id=template_id), headers=headers)
    except Exception:
        worker_logger.error(
            f"Произошла ошибка удаления шаблона id {template_id}", exc_info=True)
