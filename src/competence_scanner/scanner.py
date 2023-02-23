from jira_requests.issue.issue_request import ISSUE_REQUEST
import requests
from os import environ
from logger_config.logger_data import create_logger

scanner_logger = create_logger(__name__)

try:
    JIRA_HOST = environ["JIRA_HOST"]
    JIRA_AUTH_TOKEN = environ["JIRA_AUTH_TOKEN"]
except Exception:
    scanner_logger.critical(
        "Не обнаружена одна из переменных окружения", exc_info=True)
    exit()

#TODO уточнить за какое время нужно выбирать талоны
def get_issues_data(startAt:int = 0) -> list:
    """Забираем все тикеты зарезовленные тикеты за 30 дней

    Args:
        startAt (int, optional): порядковый номер, с которого начать . Defaults to 0.

    Returns:
        list: список тикетов по запросу
    """
    headers = {"Authorization": "Bearer {token}".format(
            token=JIRA_AUTH_TOKEN), "Accept": "application/json"}
    
    query = {
    'jql': 'resolutiondate > -30d',
    'maxResults': 1000,
    'startAt':startAt, 
    'fields':'assignee,customfield_15553'
    }
    try:
        scanner_logger.info(f"Запрашиваем талоны с параметром startAt={startAt}")
        with requests.Session() as request:
            response = request.get(ISSUE_REQUEST.format(
                    jira_host=JIRA_HOST), headers=headers,params=query)
    except Exception:
        scanner_logger.error(f"Произошла ошибка при запросе с параметром {startAt}", exc_info=True)
    
    return response.json()["issues"]


def users_with_competences() -> dict:
    """Выдергиваем из списка талонов пользователей
    и проставленные компетенции

    Returns:
        dict: ключ пользователи, значение список их компетенций
    """
    result_users = {}
    page = 0
    scanner_logger.info("Начинаем формировать компетенции пользователей")
    while True:
        issues = get_issues_data(startAt=page)
        for issue in issues:
            assignee_name = issue["fields"]["assignee"]["displayName"]
            if assignee_name and (assignee_name not in result_users):
                result_users[assignee_name] = set()
            for competence in issue["fields"]["customfield_15553"]:
                if competence["checked"]:
                    result_users[assignee_name].add(competence["name"])
        if len(issues) < 1000:
            break
        page += 1000

    for name,competences in result_users.items():
        result_users[name] = list(competences)

    return result_users