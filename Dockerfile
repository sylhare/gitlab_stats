FROM python:3.6.6

ARG token
ARG proxy
ARG gitlab

COPY . /app
WORKDIR /app

ENV GITLAB_TOKEN=$token
ENV GITLAB_URL=$gitlab
ENV HTTP_PROXY=$proxy

RUN pip install -r requirements.txt
RUN python setup.py install

# docker build -t gitlab_stats . --build-arg token="your token" --build-arg proxy="your proxy" --build-arg gitlab="gitlab url"
# docker run -it exec gitlab_stats bash gitlab_stats project_id -u url -p proxy

