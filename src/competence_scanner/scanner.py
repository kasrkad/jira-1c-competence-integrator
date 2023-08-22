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

def get_issues_data(startAt:int = 0,jql:str="'Competences Checklist' is not null AND statusCategory = Done AND resolutiondate > startOfMonth() ORDER BY updated DESC") -> list:
    """Забираем все тикеты зарезовленные тикеты c начала месяца
    или по указанным границам даты
    Args:
        startAt (int, optional): порядковый номер, с которого начать . Defaults to 0.

    Returns:
        list: список тикетов по запросу
    """
    issues_result = []
    headers = {"Authorization": "Bearer {token}".format(
            token=JIRA_AUTH_TOKEN), "Accept": "application/json"}
    
    query = {
    'jql': jql,
    'maxResults': 1000,
    'startAt':startAt, 
    'fields':'assignee,customfield_15950,issuetype,parent'
    }
    try:
        scanner_logger.info(f"Запрашиваем талоны с параметром startAt={startAt}")
        with requests.Session() as request:
            response = request.get(ISSUE_REQUEST.format(
                    jira_host=JIRA_HOST), headers=headers,params=query)
            if not response.ok:
                raise (ValueError(f'Проверьте параметры запроса для поиска ответ от = {response.text}'))
            issues_result += response.json()["issues"]
            print("найдено - ",len(response.json()["issues"]))
            if (len(response.json()["issues"])) == 1000:
                return issues_result + get_issues_data(jql=jql,startAt=startAt+1000)

    except Exception:
        scanner_logger.error(f"Произошла ошибка при запросе талонов", exc_info=True)
        raise
    return issues_result 


def isSubtask(task):
    if task["fields"]["issuetype"]["subtask"] == True:
        return True
    return False

def isParentResolve(task):
    if task["fields"]["parent"]["fields"]["status"]["name"] == "Resolved":
        return True
    return False

def users_with_competences(competence_codes:dict, issues:dict) -> dict:
    """Выдергиваем из списка талонов пользователей
    и проставленные компетенции

    Returns:
        dict: ключ пользователи, значение список их компетенций
    """
    scanner_logger.info("пришло тикетов - ", len(issues))
    scanner_logger.info("Начинаем формировать компетенции пользователей")
    assignee = {}
    for issue in issues:
        try:
            assignee_name = issue["fields"]["assignee"]["displayName"]
            assignee_email = issue["fields"]["assignee"]["emailAddress"]
            issue_key = issue["key"]
            field = issue["fields"]["customfield_15950"]
        except TypeError:
            continue
        except KeyError:
            scanner_logger.error(f"В заявке {issue_key} не найдено поле с компетенциями customfield_15950, пропускаем")
            continue

        if isSubtask(issue):
            scanner_logger.info(f"{issue['key']} is subtask!")
            if not isParentResolve(issue):
                scanner_logger.info(f"{issue['key']} Parent task not resolved! Task was skipped")
                continue

        if assignee_email and (assignee_email not in assignee):
            assignee[assignee_email] = dict()
            assignee[assignee_email]["user_name"] = assignee_name
            assignee[assignee_email]["tasks"] = []
        user_task = []
        profiles_data = []
        jira_tasks = {}
        jira_tasks["profiles"] = []
        issue_competences = []
        header_code_old = None
        
        for competence in issue["fields"]["customfield_15950"]:
        
            if competence['isHeader']:
                header_code = competence_codes.get(competence['name'], None)
                scanner_logger.info(f"Новый Заголовок найден {issue_key}! {competence['name']} - {header_code}")
                scanner_logger.info(f"Записываем предыдущий талон " + str({"profile_id":header_code_old,"competences":issue_competences}))
                
                if header_code is None:
                    scanner_logger.warn(f"В талоне {issue_key} проблема с профилем, {competence['name']}  вероятно невозможно определить код профиля")
                    if issue_competences:
                        scanner_logger.warn(f"В талоне {issue_key} проблема с профилем, но есть заполненные компетенции, очищаем") 
                        issue_competences = []
                    continue
                else:
                    if issue_competences:
                        if header_code is None:
                            scanner_logger.info(f"Не обнаружен профиль для {issue_key} - {competence['name']}")
                        if header_code_old is not None:    
                            profiles_data.append({"profile_id":header_code_old,"competences":issue_competences})
                        else:
                            scanner_logger.info(f"Для предыдущего профиля не было обнаружено кода {header_code_old}")
                        header_code_old = header_code
                        issue_competences = []
                    else:
                        header_code_old = header_code
                        continue
            if competence_codes.get(competence["name"]):
                issue_competences.append({"id":competence_codes.get(competence["name"]),"checked":competence["checked"]})
            else:
                scanner_logger.warn(f"В талоне {issue_key}, не определен id компетенции <{competence['name']}>")
        
        if issue_competences and header_code_old:
            profiles_data.append({"profile_id":header_code_old,"competences":issue_competences})
        if profiles_data:
            user_task.append({"jira_task":issue_key,"profiles": profiles_data})
        
        if user_task:
            assignee[assignee_email]["tasks"].append(*user_task)

    return assignee
