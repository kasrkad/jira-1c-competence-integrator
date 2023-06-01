from os import environ
import json
import requests
from logger_config.logger_data import create_logger
from jira_requests.templates.template_requests import GET_ALL_PROJECTS, \
    TEMPLATE_ENDPOINT, TEMPLATE_ID_ENDPOINT

worker_logger = create_logger(__name__)

try:
    JIRA_HOST = environ["JIRA_HOST"]
    JIRA_AUTH_TOKEN = environ["JIRA_AUTH_TOKEN"]
except Exception:
    worker_logger.critical(
        "Не обнаружена одна из переменных окружения", exc_info=True)
    exit()


def jira_get_all_projects() -> dict:
    """Запрашиваем все проекты из jira с их id
    Returns:
        dict: словарь с именами проектов выгруженными из jira как ключ и 
        значения в виде их id"""
    headers = {"Authorization": "Bearer {token}".format(
        token=JIRA_AUTH_TOKEN), "Accept": "application/json"}
    with requests.Session() as request:
        response = request.get(GET_ALL_PROJECTS.format(
            jira_host=JIRA_HOST), headers=headers)
        if not response.ok:
            raise ValueError(
                f"При получении всех проектов для извлечения id из {JIRA_HOST} произошла ошибка, код ответа {response.status_code}")
    data = json.loads(response.text)
    result_table = {}
    for elem in data:
        if elem["name"] not in result_table:
            result_table[elem["name"]] = elem["id"]

    return result_table


def jira_get_all_templates() -> dict:
    """Запрашиваем из jira все доступные шаблоны
    Returns: 
        dict: возвращаем словарь со всеми доступными шаблонами 
    """
    headers = {"Authorization": "Bearer {token}".format(
        token=JIRA_AUTH_TOKEN), "Content-Type": "application/json"}
    with requests.Session() as request:
        response = request.get(TEMPLATE_ENDPOINT.format(
            jira_host=JIRA_HOST), headers=headers)
        if not response.ok:
            raise ValueError(
                f"Проблема при запросе всех шаблонов из {JIRA_HOST}, код ответа {response.status_code}")
    all_templates_json = response.json()
    return all_templates_json


def checklist_updater(checklist_id: int, update_data: str) -> None:
    """Обновляем указанный шаблон
    обязатольно использовать заголовок "Content-Type": "application/x-www-form-urlencoded" 
    и приводить данные к формату строкеи кодируя в utf-8
    Args:
        checklist_id(int): id шаблона в jira для обновления
        update_data(str): строка преобразованная из json поля itemsJson"""
    HEADERS_UPDATE = {"Authorization": "Bearer {token}".format(
        token=JIRA_AUTH_TOKEN), "Content-Type": "application/x-www-form-urlencoded"}
    with requests.Session() as request:
        response = request.put(TEMPLATE_ID_ENDPOINT.format(jira_host=JIRA_HOST,
                                                           template_id=checklist_id),
                               headers=HEADERS_UPDATE,
                               data=f"itemsJson={update_data}".encode("utf-8"))
        if not response.ok:
            raise ValueError(f"Произошла ошибка при обновлении шаблона  {checklist_id}, itemsJson={update_data}")


def checklist_loader(checklist_data: dict) -> None:
    """Загружаем ранее несуществующий шаблон
    Args:
        checklist_data(dict): словарь с данными по шаблону чеклиста готовыми к загрузке"""
    headers = {"Authorization": "Bearer {token}".format(
        token=JIRA_AUTH_TOKEN), "Content-Type": "application/json"}
    with requests.Session() as request:
        response = request.post(TEMPLATE_ENDPOINT.format(jira_host=JIRA_HOST),
                                headers=headers, data=json.dumps(checklist_data))
        if not response.ok:
            raise ValueError(
                f'Проблема при создании шаблона код ответа {response.status_code} текст ошибки {response.text}\n {checklist_data}')
   

def checklist_delete(template_id: int) -> None:
    """Удаляем шаблон чеклиста из jira
    Args:
        template_id(int): id шаблона чеклиста для удаления"""
    headers = {"Authorization": "Bearer {token}".format(
        token=JIRA_AUTH_TOKEN)}
    with requests.Session() as request:
        response = request.delete(TEMPLATE_ID_ENDPOINT.format(
            jira_host=JIRA_HOST, template_id=template_id), headers=headers)
