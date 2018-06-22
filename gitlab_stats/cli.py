# !/usr/bin/python
# -*- coding: utf-8 -*-
"""
Gitlab_stats:

Generate a report from gitlab's pipeline metrics

for help:    gitlab_stats -h
example:     gitlab_stats 4895805
example:     gitlab_stats 123 -s "https://my_gitlab.com"
"""
import sys
import argparse
from gitlab_stats import utils
from gitlab_stats.wrapper import API


def parse_args(args):
    parser = argparse.ArgumentParser(description="gitlab-stats: Generate a report from gitlab's pipeline metrics")
    parser.add_argument("id",
                        help="Put the id of the gitlab project")
    parser.add_argument("-r", "--report",
                        action="store_true",
                        dest="report",
                        default=False,
                        help="Generate a report in csv")
    parser.add_argument("-u", "--url",
                        default=['https://gitlab.com'],
                        nargs=1,
                        help="Put the url of your gitlab instance if different from https://gitlab.com")
    parser.add_argument("-p", "--proxy",
                        default=[''],
                        nargs=1,
                        help="Add the url of your proxy like 'http://my.proxy.url:8083'")

    return parser.parse_args(args)


def print_report(project_id, url, proxy):
    proxy = utils.format_proxy(proxy)
    gitlab = API(base_url=url, proxies=proxy)
    utils.print_cli_report(gitlab.get_enhanced_project_info(project_id))


def main():
    args = parse_args(sys.argv[1:])
    print_report(args.id, args.url[0], args.proxy[0])

    if args.report:
        print("Reports not yet implemented ¯\_(ツ)_/¯")


if __name__ == '__main__':
    main()
