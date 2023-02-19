from logger_config.logger_data import create_logger
from template_worker.worker import checklist_delete, checklist_updater,\
    jira_get_all_projects, jira_get_all_templates, checklist_loader
from json_operator.operator import load_1c_data_from_file, get_competence_codes,\
    jira_id_for_1c, data_from_1c_compare, data_from_jira_compare


main_logger = create_logger(__name__)


def main():
    try:
        all_templates = jira_get_all_templates()
        main_logger.info("getting all jira projects")
        projects = jira_get_all_projects()
        main_logger.info("load data from 1c.json")
        data_from_1c = load_1c_data_from_file("1c_test.json")
        main_logger.info("create jira projects with ids list")
        project_jira_id = jira_id_for_1c(
            data_1c=data_from_1c, data_jira=projects)
        main_logger.info("creating list with templates from 1c file")
        comparing_1c = data_from_1c_compare(
            data_1c=data_from_1c, jira_id=project_jira_id)

        main_logger.info("creating list with templates from jira")
        comparing_jira = data_from_jira_compare(all_templates)

        need_create = 0
        need_update = 0
        main_logger.info("checking templates for create and update")
        for project_template_name, project_data in comparing_1c.items():
            if project_template_name not in comparing_jira:
                checklist_loader(checklist_data=project_data)
                need_create += 1
            else:
                checklist_updater(
                    checklist_id=comparing_jira[project_template_name],
                    update_data=project_data["itemsJson"])
                need_update += 1

        main_logger.info(f"Created {need_create}, updated {need_update}")
    except Exception:
        main_logger.critical(
            "В основном потоке произошла ошибка", exc_info=True)
        exit()


if __name__ == "__main__":
    main()
