#POST Create template 
#Content-Type: application/json
#Authorization: Bearer {{token}}
CREATE_TEMPLATE = "https://{jira_host}/rest/com.okapya.jira.checklist/latest/templates/"

#GET
#Authorization: Bearer {{token}}
GET_PROJECT_TEMPLATES = "https://{jira_host}/rest/com.okapya.jira.checklist/latest/projects/15135/templates"

#GET
#Authorization: Bearer {{token}}
GET_TEMPLATE_BY_ID = "https://{jira_host}/rest/com.okapya.jira.checklist/latest/templates/{template_id}"

#GET
#Authorization: Bearer {{token}}
GET_ALL_TEMPLATES = "https://{jira_host}/rest/com.okapya.jira.checklist/latest/templates"