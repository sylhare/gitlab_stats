import time
import unittest

import tests
from gitlab_stats.wrapper import API
from tests.mock_server import start_mock_server, get_free_port, MockGitlabServer


class WrapperTest(unittest.TestCase):

    def setUp(self):
        self._started_at = time.time()
        self.mock_server_port = get_free_port()
        start_mock_server(self.mock_server_port, MockGitlabServer)
        mock_users_url = 'http://localhost:{port}'.format(port=self.mock_server_port)
        self.gaw = API(base_url=mock_users_url, proxies=tests.PROXIES)

    def tearDown(self):
        elapsed = time.time() - self._started_at
        print('({}s) - {}'.format(round(elapsed, 2), self.id()[36:]))

    # -- API connexion and information retrieve

    @tests.api_call
    def test_002_get_response(self):
        response = self.gaw.get(API.PROJECT_URL)
        self.assertEqual(response.status_code, 200,
                         "Can't reach this url, it can be your proxy or a wrong token, set them in a .env file")

    @tests.api_call
    def test_004_wrong_token_raise_error(self):
        with self.assertRaises(ConnectionError):
            self.gaw._header = {'Content-Type': 'application/json', 'PRIVATE-TOKEN': '{}'.format("wrong token")}
            self.gaw.get_project_name(tests.PROJECT_ID)

    # -- Get project info

    @tests.api_call
    def test_010_get_project_name_from_id(self):
        response = self.gaw.get_project_name(tests.PROJECT_ID)
        self.assertEqual(response, tests.PROJECT_NAME)

    @tests.api_call
    def test_011_get_all_projects(self):
        response = self.gaw.get_all_projects(1)
        self.assertEqual(type(response), list)
        self.assertEqual(type(response[0]), dict, "Project id and name should be in a dict")

    @tests.api_call
    def test_012_get_all_projects_and_correct_fields(self):
        response = self.gaw.get_all_projects(1)
        self.assertTrue('id' in response[0])
        self.assertTrue('name' in response[0])

    @tests.api_call
    def test_013_get_project_information(self):
        response = self.gaw.get_basic_project_info(tests.PROJECT_ID)
        self.assertEqual(len(response), 3)
        self.assertTrue('id' in response)
        self.assertTrue('name' in response)
        self.assertTrue('pipelines' in response)

    @tests.api_call
    def test_014_get_enhanced_project_information(self):
        response = self.gaw.get_enhanced_project_info(tests.PROJECT_ID)
        self.assertEqual(len(response), 5)
        self.assertTrue('id' in response)
        self.assertTrue('name' in response)
        self.assertTrue('duration_moy' in response)
        self.assertTrue('duration_in_minutes' in response)
        self.assertTrue('success_percentage' in response)

    @tests.api_call
    def test_015_get_project_report_from_id(self):
        self.gaw.get_stats_report(tests.PROJECT_ID)

    # -- Get pipeline info

    @tests.api_call
    def test_020_get_all_pipelines_of_a_project(self):
        response = self.gaw.get_all_pipelines_id(tests.PROJECT_ID)
        self.assertEqual(type(response), list)
        self.assertEqual(type(response[0]), int, "Pipeline id should be a int")

    @tests.api_call
    def test_021_get_all_pipelines_info_of_a_project(self):
        response = self.gaw.get_all_pipelines_info(tests.PROJECT_ID)
        self.assertEqual(type(response), list)
        self.assertEqual(type(response[0]), dict, "Pipeline info should be a dict")

    @tests.api_call
    def test_022_get_all_pipelines_info_and_correct_fields(self):
        response = self.gaw.get_all_pipelines_info(tests.PROJECT_ID)
        self.assertTrue('id' in response[0])
        self.assertTrue('status' in response[0])
        self.assertTrue('duration' in response[0])
        self.assertTrue('date' in response[0])


if __name__ == "__main__":
    unittest.main()
