FROM python:3.10.9-alpine3.16 as builder
RUN apk update \
    && apk upgrade \
    && apk add --no-cache bash \
    libffi-dev \
    gcc \
    musl-dev
COPY ./requirements.txt /jira_integrator/
WORKDIR /jira_integrator/
RUN cd /jira_integrator/ && pip3 install -r requirements.txt 

FROM python:3.10.9-alpine3.16
ENV TZ="Asia/Yekaterinburg"
ENV JIRA_HOST=""
ENV JIRA_AUTH_TOKEN=""
RUN apk update \
    && apk upgrade 
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY ./src /jira_integrator
WORKDIR /jira_integrator/
ENTRYPOINT ["python", "main.py"]