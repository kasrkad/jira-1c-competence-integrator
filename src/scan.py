from competence_scanner.scanner import users_with_competences,get_issues_data
from logger_config.logger_data import create_logger
from json_operator.operator import get_competence_codes,load_1c_data_from_file
import json
from datetime import datetime
from json2xml import json2xml
from json2xml.utils import readfromstring



scan_logger = create_logger(__name__)

now = datetime.now()
date_time = now.strftime("%Y.%m.%d")


codes = get_competence_codes(load_1c_data_from_file("./1c/1c.json"))
issues_data = get_issues_data(jql="issue in (EO-5291,EO-5305,MES-2481,MES-4520,MES-4823)")

with open('comp.json', 'w', encoding='utf8') as f:
    json.dump(codes, f, ensure_ascii=False,indent=2)

with open('res.json', 'w', encoding='utf8') as f:
    json.dump(issues_data, f, ensure_ascii=False,indent=2)
users_competences = users_with_competences(competence_codes=codes,issues=issues_data)
data = json.dumps({"date":date_time, "competence_block":users_competences},ensure_ascii=False)
xml_data = readfromstring(data)
with open("result_xml.xml", 'w',encoding="utf-8") as outfile:
    outfile.write(json2xml.Json2xml(xml_data, wrapper="all", pretty=True).to_xml())