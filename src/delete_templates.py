from logger_config.logger_data import create_logger
from template_worker.worker import checklist_delete, checklist_updater,\
    jira_get_all_projects, jira_get_all_templates, checklist_loader
from json_operator.operator import load_1c_data_from_file, get_competence_codes,\
    jira_id_for_1c, data_from_1c_compare, data_from_jira_compare


main_logger = create_logger(__name__)


def main():
    try:
        main_logger.info("getting all jira templates")
        all_templates = jira_get_all_templates()
        for template in all_templates["templates"]:
            print(template["name"],template["customFieldId"])
            checklist_delete(template["id"])
    except Exception:
        main_logger.critical(
            "В основном потоке произошла ошибка", exc_info=True)
        exit()


if __name__ == "__main__":
    main()
