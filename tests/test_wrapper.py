import tests
import time
import unittest
from gitlab_stats.utils import *
from gitlab_stats.wrapper import API


class APITest(unittest.TestCase):

    def setUp(self):
        self.gaw = API(base_url="https://gitlab.com", proxies=tests.PROXIES)
        self._started_at = time.time()

    def tearDown(self):
        elapsed = time.time() - self._started_at
        print('({}s) - {}'.format(round(elapsed, 2), self.id()[36:]))

    # -- API connexion and information retrieve

    def test_001_check_proxy_format(self):
        result = format_proxy("test")
        self.assertEqual({'http': "test", 'https': "test"}, result)

    @tests.api_call
    def test_002_get_response(self):
        response = self.gaw.get(API.PROJECT_URL)
        self.assertEqual(response.status_code, 200,
                         "Can't reach this url, it can be your proxy or a wrong token, set them in a .env file")

    def test_003_no_token_raise_error(self):
        with self.assertRaises(KeyError):
            """ Can't really test this """
            import os
            print(os.environ["NOT_WHERE_TOKEN_IS_STORED"])  # This will raise a key error
            API(base_url="https://gitlab.com", proxies=tests.PROXIES)  # key error when no token in GITLAB_TOKEN

    @tests.api_call
    def test_004_wrong_token_raise_error(self):
        with self.assertRaises(ConnectionError):
            self.gaw._header = {'Content-Type': 'application/json', 'PRIVATE-TOKEN': '{0}'.format("wrong token")}
            self.gaw.get_project_name(tests.PROJECT_ID)

    # -- Get project info

    @tests.api_call
    def test_010_get_project_name_from_id(self):
        response = self.gaw.get_project_name(tests.PROJECT_ID)
        self.assertEquals(response, tests.PROJECT_NAME)

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
        response = self.gaw.get_all_pipelines_id_of(tests.PROJECT_ID)
        self.assertEqual(type(response), list)
        self.assertEqual(type(response[0]), int, "Pipeline id should be a int")

    @tests.api_call
    def test_021_get_all_pipelines_info_of_a_project(self):
        response = self.gaw.get_all_pipelines_info_of(tests.PROJECT_ID)
        self.assertEqual(type(response), list)
        self.assertEqual(type(response[0]), dict, "Pipeline info should be a dict")

    @tests.api_call
    def test_022_get_all_pipelines_info_and_correct_fields(self):
        response = self.gaw.get_all_pipelines_info_of(tests.PROJECT_ID)
        self.assertTrue('id' in response[0])
        self.assertTrue('status' in response[0])
        self.assertTrue('duration' in response[0])
        self.assertTrue('date' in response[0])

    # -- Project name and id

    def test_030_get_name_and_id_in_a_list_of_dict(self):
        response = get_name_and_id(tests.PROJECT)
        self.assertEqual(type(response), list)
        self.assertEqual(type(response[0]), dict)

    def test_031_get_name_and_id_has_correct_fields(self):
        response = get_name_and_id(tests.PROJECT)
        self.assertEqual(len(response[0]), 2)
        self.assertEqual(response[0]['id'], tests.PROJECT_ID)
        self.assertEqual(response[0]['name'], tests.PROJECT_NAME)

    # -- Pipeline

    def test_040_get_pipeline_id_in_a_list(self):
        response = get_pipelines_id(tests.PIPELINES)
        self.assertEqual(type(response), list)

    def test_041_get_pipeline_id_in_a_dict_has_correct_fields(self):
        response = get_pipelines_id(tests.PIPELINES)
        self.assertEqual(type(response), list)
        self.assertEqual(len(response), 4)
        self.assertEqual(response[0], 34692)

    def test_042_get_pipeline_info_in_a_dict(self):
        response = get_pipeline_info(tests.PIPELINE_INFO)
        self.assertEqual(type(response), dict)

    def test_043_get_pipeline_info_with_correct_fields(self):
        response = get_pipeline_info(tests.PIPELINE_INFO)
        self.assertEqual(len(response), 4)
        self.assertTrue('id' in response)
        self.assertTrue('status' in response)
        self.assertTrue('duration' in response)
        self.assertTrue('date' in response)

    # -- Value added

    def test_050_get_moy_duration(self):
        duration_moy = get_duration_moy(tests.PROJECT_INFO)
        self.assertEqual(duration_moy, 58.9)

    def test_051_get_moy_duration_with_null(self):
        duration_moy = get_duration_moy(tests.PROJECT_INFO_WITH_ONE_DURATION_NONE)
        self.assertEqual(duration_moy, 57.7)

    def test_052_get_moy_duration_when_one_duration_null(self):
        duration_moy = get_duration_moy(tests.PROJECT_INFO_DURATION_NONE)
        self.assertEqual(duration_moy, None)

    def test_053_get_success_percentage(self):
        success_percentage = get_success_percentage(tests.PROJECT_INFO)
        self.assertEqual(success_percentage, 70)

    def test_054_get_success_percentage_when_no_pipeline(self):
        success_percentage = get_success_percentage(tests.PROJECT_INFO_EMPTY)
        self.assertEqual(success_percentage, None)

    def test_055_get_all_pipeline_info_from_2_weeks_ago(self):
        response = get_pipeline_info_from(tests.PROJECT_INFO_TIME, 15)
        self.assertEqual(len(response['pipelines']), 6)

    def test_056_enhance_project_info(self):
        response = enhance_project_info(tests.PROJECT_INFO)
        self.assertEqual(len(response), 5)
        self.assertTrue('id' in response)
        self.assertTrue('name' in response)
        self.assertTrue('duration_moy' in response)
        self.assertTrue('duration_in_minutes' in response)
        self.assertTrue('success_percentage' in response)

    def test_57_get_report(self):
        print_cli_report(tests.PROJECT_INFO_ENHANCED)


if __name__ == "__main__":
    unittest.main()
