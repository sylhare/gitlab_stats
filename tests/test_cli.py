import os
import unittest
from unittest.mock import patch

import tests
from gitlab_stats.cli import *
from tests.mock_server import start_mock_server, get_free_port, MockGitlabServer


class CLITest(unittest.TestCase):

    def setUp(self):
        self.mock_server_port = get_free_port()
        start_mock_server(self.mock_server_port, MockGitlabServer)
        self.mock_users_url = 'http://localhost:{port}'.format(port=self.mock_server_port)

    def test_100_run_main(self):
        result = os.system("python {}/gitlab_stats/cli.py -h".format(tests.ROOT_PATH))
        self.assertEqual(result, 0)

    @tests.api_call
    def test_101_print_report(self):
        test_args = ['', '-r', str(tests.PROJECT_ID), '-u', self.mock_users_url]
        with patch.object(sys, 'argv', test_args):
            main()
        self.assertTrue(os.path.isfile('output.csv'))

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
