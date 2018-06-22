import os
import csv
import tests
import unittest
from gitlab_stats.cli import *
from unittest.mock import patch


class CLITest(unittest.TestCase):

    def setUp(self):
        pass

    @tests.api_call
    def test_100_parse_args(self):
        if tests.PROXY:
            testargs = ['', str(tests.PROJECT_ID), '-p', tests.PROXY]
        else:
            testargs = ['', str(tests.PROJECT_ID)]
        with patch.object(sys, 'argv', testargs):
            main()

    @tests.api_call
    def test_101_print_report(self):
        print_report(str(tests.PROJECT_ID), 'https://gitlab.com', tests.PROXY)

    def test_200_parser_id(self):
        parser = parse_args(['123'])
        self.assertEqual(parser.id, '123')
        self.assertFalse(parser.report)
        self.assertEqual(parser.url, ['https://gitlab.com'])
        self.assertEqual(parser.proxy, [''])

    def test_201_parser_id_with_url(self):
        parser = parse_args(['123', '-u', 'https://myurl.com'])
        self.assertEqual(parser.url, ['https://myurl.com'])

    def test_202_parser_id_with_report(self):
        parser = parse_args(['123', '-r'])
        self.assertTrue(parser.report)

    def test_203_parser_id_with_proxy(self):
        parser = parse_args(['123', '-p', 'https://myproxy.com'])
        self.assertEqual(parser.proxy, ['https://myproxy.com'])

    def test_210_parser_id_with_url_and_report(self):
        parser = parse_args(['123', '-r', '-u', 'https://myurl.com'])
        self.assertTrue(parser.report)
        self.assertEqual(parser.url, ['https://myurl.com'])

    def test_211_parser_id_with_url_and_report_and_proxy(self):
        parser = parse_args(['123', '-r', '-u', 'https://myurl.com', '-p', 'https://myproxy.com'])
        self.assertTrue(parser.report)
        self.assertEqual(parser.url, ['https://myurl.com'])
        self.assertEqual(parser.proxy, ['https://myproxy.com'])

    def test_220_create_a_csv(self):
        utils.create_dict_to_csv(tests.PROJECT_INFO_ENHANCED, 'output.csv')
        self.assertTrue(os.path.isfile('output.csv'))

    def test_221_write_into_a_created_report_do_not_had_headers(self):
        utils.write_dict_to_csv(tests.PROJECT_INFO_ENHANCED, 'output.csv')
        with open('output.csv', 'r') as f:
            result = list(csv.reader(f))
            self.assertNotEqual(result[0], result[2])

    def test_222_report_regenerated(self):
        utils.generate_report(tests.PROJECT_INFO_ENHANCED, 'output.csv')
        with open('output.csv', 'r') as f:
            result = list(csv.reader(f))
            self.assertEqual(result[2], result[3])
        os.remove('output.csv')

    def test_223_report_generated(self):
        utils.generate_report(tests.PROJECT_INFO_ENHANCED, 'output.csv')
        with open('output.csv', 'r') as f:
            result = list(csv.reader(f))
            self.assertNotEqual(result[0], result[1])
            with self.assertRaises(IndexError):
                report_created_so_only_two_rows = result[2]
        os.remove('output.csv')


if __name__ == "__main__":
    unittest.main()
