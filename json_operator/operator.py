import json
from logger_config.logger_data import create_logger

operator_logger = create_logger(__name__)

def load_1c_data_from_file(filename:str)-> dict:
    """Грузим данные с файла выгрузки из 1с

    Args:
        filename (str): имя файла

    Returns:
        dict: возвращает словарь выгруженный из файла
    """
    operator_logger.info(f'Загружаем данные из файла выгрузки 1с')
    try:
        with open(filename,'r',encoding='utf-8-sig')  as json_file:
            data_1c = json.load(json_file)
    except Exception:
        operator_logger.error(f"Ошибка при загрузке файла {filename}", exc_info=True)
        raise
    return data_1c


def get_jira_id_for_1c_projects(data_1c:dict, data_jira:dict) -> dict:
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

