import os
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
            result = main()
            self.assertEqual(result, 0)

    @tests.api_call
    def test_101_print_report(self):
        if tests.PROXY:
            testargs = ['', str(tests.PROJECT_ID), '-p', tests.PROXY, '-r']
        else:
            testargs = ['', str(tests.PROJECT_ID), '-r']
        with patch.object(sys, 'argv', testargs):
            main()
            self.assertTrue(os.path.isfile('output.csv'))

    def test_102_run_main(self):
        result = os.system("python "+tests.ROOT_PATH+"/gitlab_stats/cli.py -h")
        self.assertEqual(result, 0)

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


if __name__ == "__main__":
    unittest.main()
