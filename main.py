from logger_config.logger_data import create_logger
from template_worker.worker import jira_get_all_projects, jira_get_all_templates, template_loader, delete_template
from json_operator.operator import load_1c_data_from_file, jira_id_for_1c, convert_json_for_jira, get_competence_codes

main_logger = create_logger(__name__)


def main():
    try:
        all_templates = jira_get_all_templates()
        main_logger.info("getting all jira projects")
        projects = jira_get_all_projects()
        main_logger.info("load data from 1c.json")
        data_from_1c = load_1c_data_from_file("1c.json")
        competence_codes = get_competence_codes(data_from_1c)
        main_logger.info("get correct project ids from jira")
        project_jira_id = jira_id_for_1c(
            data_1c=data_from_1c, data_jira=projects)
        main_logger.info("convert data for template uploading")
        data_for_upload = convert_json_for_jira(
            data_1c=data_from_1c, jira_id=project_jira_id)
        main_logger.info("upload_template")
        for template in all_templates["templates"]:
            print(template)
        template_loader(data_for_upload)

        for template in all_templates["templates"]:
            print(template["id"])
            delete_template(template["id"])

    except Exception:
        main_logger.critical(
            "В основном потоке произошла ошибка", exc_info=True)


if __name__ == "__main__":
    main()

    # print(all_templates)
    # TODO обновляем шаблоны
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
