from competence_scanner.scanner import users_with_competences
from logger_config.logger_data import create_logger


scan_logger = create_logger(__name__)

users_competences = users_with_competences()
#TODO здесь будет формирование выгрузки для 1с, когда предоставят формат