import tests
import unittest
from gitlab_stats.utils import *


class UtilsTest(unittest.TestCase):

    def test_001_check_proxy_format(self):
        result = format_proxy("test")
        self.assertEqual({'http': "test", 'https': "test"}, result)

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