#!/usr/bin/python
# __author__ = 'JasonSheh'
# __email__ = 'qq3039344@gmail.com'
# -*- coding:utf-8 -*-

# !/usr/bin/python
# __author__ = 'jasonsheh'
# -*- coding:utf-8 -*-

"""
对所有脚本进行统一规划管理
"""

from database.srcList import SrcList
from database.database import Database
from database.gitLeak import GitLeak

from lib.info.subdomain import AllDomain
from lib.info.siteinfo import SiteInfo
from lib.info.sendir import SenDir

from lib.poc.common.xss import Xss
from lib.poc.common.sqli import SqlInjection
from lib.poc.common.struts2 import Struts2

from lib.git.gitscan import GitScan
from lib.crawler import Crawler

from setting import sudomain_scan_size, github_scan_size


class SRCKiller:
    def __init__(self):
        self.src_scan_list = SrcList().select_un_scan_src_list(sudomain_scan_size)

    def info_collect(self):
        for domain in self.src_scan_list:
            src_id = domain['src_id']
            domain_id = domain['id']
            url = domain['url']
            domain = domain['url'][2:]

            domains = AllDomain(domain).run()

            print(len(domains.keys()))

            info = SiteInfo([x for x in domains.keys()]).run()
            Database().insert_subdomain(domains, info, domain_id, src_id)
            SrcList().update_scan_time(url)

    def git_leak(self):
        rules = GitLeak().select_rules(count=github_scan_size)
        for rule in rules:
            leak = {"domain_id": rule["domain_id"], "domain": rule["domain"]}
            print(rule)
            leak[""] = GitScan(rule['domain'])
            GitLeak().insert_leak(leak)


if __name__ == '__main__':
    SRCKiller().git_leak()
