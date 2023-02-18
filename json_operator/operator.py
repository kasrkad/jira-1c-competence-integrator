import json
from logger_config.logger_data import create_logger

operator_logger = create_logger(__name__)


def load_1c_data_from_file(filename: str) -> dict:
    """Грузим данные с файла выгрузки из 1с

    Args:
        filename (str): имя файла

    Returns:
        dict: возвращает словарь выгруженный из файла
    """
    operator_logger.info(f'Загружаем данные из файла выгрузки 1с {filename}')
    try:
        with open(filename, 'r', encoding='utf-8-sig') as json_file:
            data_1c = json.load(json_file)
    except Exception:
        operator_logger.error(f"Ошибка при загрузке файла {filename}",
                              exc_info=True)
        raise
    return data_1c


def jira_id_for_1c(data_1c: dict, data_jira: dict) -> dict:
    """Сопоставляем проекты с 1с с id проектов в jira

    Args:
        data_1c (dict): данные выгрузки из 1с
        data_jira (dict): данные с проектами из jira

    Returns:
        dict: _description_
    """
    result_pairs = {}
    for elem in data_1c:
        result_pairs[elem["name"]] = data_jira.get(elem["name"], None)
    return result_pairs


def get_competence_codes(data_1c):
    competence_codes = {}
    for project in data_1c:
        for profiles in project["profiles"]:
            for competence in profiles["competences"]:
                if competence["id"] not in competence_codes:
                    competence_codes[competence["name"]] = competence["id"]
    return competence_codes


def convert_json_for_jira(data_1c: dict, jira_id: dict) -> dict:
    result_data = []
    for project in data_1c:
        jira_project_id = jira_id.get(project["name"], None)
        if not jira_project_id:
            operator_logger.error(f"for {project['name']}\
                    id is {jira_project_id}, must be not None")
            continue

        for profile in project["profiles"]:
            base_json = {"fieldConfigId": 17262,
                         "items": None, "importable": True,
                         "customFiledId": 15553}
            # добавляем поле с id в результирующий json
            base_json["project"] = jira_project_id
            template_name = f"{profile['functionalDirection']}|{profile['name']}"
            base_json["name"] = template_name  # добавляем имя шаблона
            competences = [
                {"id": "-1", "name": template_name, "isHeader": True}]
            competences += profile["competences"]
            for elem in competences:
                elem["mandatory"] = False
            base_json["itemsJson"] = str(
                json.dumps(competences, ensure_ascii=False))

            result_data.append(base_json)
    return result_data
