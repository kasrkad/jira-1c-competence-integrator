from logger_config.logger_data import create_logger
from template_worker.worker import *
from json_operator.operator import *
from config import *

main_logger = create_logger(__name__)



main_logger.info("getting all jira projects")

projects = get_all_jira_project()

main_logger.info('get all jira templates')
all_templates = get_all_jira_templates()

data_from_1c = load_1c_data_from_file("1c.json")

project_jira_id = get_jira_id_for_1c_projects(data_1c=data_from_1c, data_jira=projects)


for elem in data_from_1c:
    print(elem["profiles"])




#TODO обновляем шаблоны
# new_session = requests.Session()
# HEADERS_UPDATE = {"Authorization": "Bearer {token}".format(token=JIRA_AUTH_TOKEN),"Content-Type": "application/x-www-form-urlencoded"}
# new_response = new_session.put(UPDATE_TEMPLATE.format(jira_host=JIRA_HOST,template_id=id),
#                             headers=HEADERS_UPDATE,data=f"itemsJson={str(json_data)}".encode("utf-8"))

# print(new_response.status_code)
# print(new_response.content)
# new_session.close()
# with open("new.json", 'w', encoding="utf-8") as out_file:
#     json.dump(new_response.json(), out_file,indent=4, ensure_ascii=False)
# session.close()