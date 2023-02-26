from competence_scanner.scanner import users_with_competences
from logger_config.logger_data import create_logger
from json_operator.operator import get_competence_codes,load_1c_data_from_file

scan_logger = create_logger(__name__)


codes = get_competence_codes(load_1c_data_from_file("./1c/1c.json"))

users_competences = users_with_competences(competence_codes=codes)
print(users_competences)
#TODO здесь будет формирование выгрузки для 1с, когда предоставят формат