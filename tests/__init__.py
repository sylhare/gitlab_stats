import os
import unittest
from datetime import datetime

api_call = unittest.skipIf(False, 'Skip the test that access the gitlab API')
ROOT_PATH = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
ENV_VAR_PATH = os.path.join(ROOT_PATH, "gitlab.env")

try:
    PROXY = os.environ["PROXY"]
except KeyError:
    PROXY = ''

PROXIES = {'http': PROXY, 'https': PROXY}

PROJECT_ID = 4895805
PROJECT_NAME = "integration-tests"

PROJECT = [
    {"id": 4895805, "description": "", "name": "integration-tests", "name_with_namespace": "integration-tests",
     "path": "path to project", "path_with_namespace": "I am getting bored of this",
     "created_at": "2018-06-08T18:18:39.029Z", "default_branch": "master",
     "forks_count": 0, "last_activity_at": "2018-06-15T14:42:54.278Z"}
]

PIPELINES = [
    {'id': 34692, "sha": "111edcb12207aec17aca660e957269fcc1a06356", "ref": "master", "status": "canceled"},
    {"id": 34501, "sha": "1cb7a4d8b1469a303dqqwe56877068610b9fdcb0", "ref": "master", "status": "success"},
    {"id": 34155, "sha": "b15e77c55bba9783fbwwqa24f17a304d86dde54c", "ref": "master", "status": "failed"},
    {"id": 32026, "sha": "6f52ae30eb543adecb81c74ca60253e62bcc586d", "ref": "master", "status": "skipped"},
]

PIPELINE_INFO = {
    "id": 33409, "sha": "d724e231065505afgwr2e6909e3baf4f90278", "ref": "master", "status": "success",
    "before_sha": "9396e122692cd0aa7a9c2dsfsb8f8efe97cc56", "tag": False, "yaml_errors": None,
    "user": {"id": 40, "name": "name", "username": "username", "state": "active"},
    "created_at": "2018-06-11T21:45:47.805Z",
    "updated_at": "2018-06-11T21:46:49.364Z", "started_at": "2018-06-11T21:45:49.574Z",
    "finished_at": "2018-06-11T21:46:49.359Z", "committed_at": None, "duration": 59, "coverage": None
}

# Duration moy - 58.9
PROJECT_INFO = {
    'id': PROJECT_ID,
    'name': PROJECT_NAME,
    'pipelines': [{'id': 34501, 'status': 'success', 'duration': 59, 'date': '2018-06-14'},
                  {'id': 34155, 'status': 'success', 'duration': 58, 'date': '2018-06-13'},
                  {'id': 33844, 'status': 'success', 'duration': 60, 'date': '2018-06-12'},
                  {'id': 33808, 'status': 'success', 'duration': 56, 'date': '2018-06-12'},
                  {'id': 33185, 'status': 'success', 'duration': 57, 'date': '2018-06-11'},
                  {'id': 33183, 'status': 'success', 'duration': 57, 'date': '2018-06-11'},
                  {'id': 33124, 'status': 'success', 'duration': 27, 'date': '2018-05-11'},
                  {'id': 31866, 'status': 'skipped', 'duration': 97, 'date': '2018-05-08'},
                  {'id': 31862, 'status': 'canceled', 'duration': 57, 'date': '2018-05-08'},
                  {'id': 31844, 'status': 'failed', 'duration': 61, 'date': '2018-05-08'}]
}

PROJECT_INFO_TIME = {
    'id': PROJECT_ID,
    'name': PROJECT_NAME,
    'pipelines': [{'id': 34501, 'status': 'success', 'duration': 59, 'date': datetime.now().strftime("%Y-%m-%d")},
                  {'id': 34155, 'status': 'success', 'duration': 58, 'date': datetime.now().strftime("%Y-%m-%d")},
                  {'id': 33844, 'status': 'success', 'duration': 60, 'date': datetime.now().strftime("%Y-%m-%d")},
                  {'id': 33808, 'status': 'success', 'duration': 56, 'date': datetime.now().strftime("%Y-%m-%d")},
                  {'id': 33185, 'status': 'success', 'duration': 57, 'date': datetime.now().strftime("%Y-%m-%d")},
                  {'id': 33183, 'status': 'success', 'duration': 57, 'date': datetime.now().strftime("%Y-%m-%d")},
                  {'id': 33124, 'status': 'success', 'duration': 27, 'date': '2018-05-11'},
                  {'id': 31866, 'status': 'skipped', 'duration': 97, 'date': '2018-05-08'},
                  {'id': 31862, 'status': 'canceled', 'duration': 57, 'date': '2018-05-08'},
                  {'id': 31844, 'status': 'failed', 'duration': 61, 'date': '2018-05-08'}]
}

PROJECT_INFO_ENHANCED = {'id': PROJECT_ID,
                         'name': PROJECT_NAME,
                         'duration_moy': 1.00,
                         'duration_in_minutes': '0 min 59s',
                         'success_percentage': 70
                         }

PROJECT_INFO_EMPTY = {
    'pipelines': []
}

PROJECT_INFO_WITH_ONE_DURATION_NONE = {
    'pipelines': [{'id': 34501, 'status': 'success', 'duration': 59, 'date': '2018-06-14'},
                  {'id': 34155, 'status': 'success', 'duration': 58, 'date': '2018-06-13'},
                  {'id': 33844, 'status': 'success', 'duration': None, 'date': '2018-06-12'},
                  {'id': 33808, 'status': 'success', 'duration': 56, 'date': '2018-06-12'}, ]
}

PROJECT_INFO_DURATION_NONE = {
    'pipelines': [{'id': 33844, 'status': 'success', 'duration': None, 'date': '2018-06-12'}]
}
