#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals
import sys
import optparse
from invoke import run

import re


class UpdateCommitMsg(object):
    """
    This hook saves developers time by prepending ticket numbers to commit-msgs.
    For this to work the following two conditions must be met:
        - The ticket format regex specified must match.
        - The branch name format must be <ticket number>_<rest of the branch name>
    """

    def __init__(self):
        self.errors = 0
        self.branch = self.get_branch_name()

    def check_file(self, filename, regex):
        self.current_filename = filename

        with open(filename[0], 'r+') as fd:
            contents = fd.readlines()
            commit_msg = contents[0]
            if not re.search(regex, commit_msg):
                # Check if we can grab jira ticket from branch name.
                if re.search(regex, self.branch):
                    jira_ticket = self.branch.split('_')[0]
                    new_commit_msg = '{} {}'.format(jira_ticket, commit_msg)
                    fd.seek(0)
                    fd.write(new_commit_msg)
                    fd.truncate()

    def get_branch_name(self):
        # Only git support for right now.
        return run("git rev-parse --abbrev-ref HEAD").stdout

    def main(self):
        parser = optparse.OptionParser(
            usage='%prog [options] file [files]',
            description='Checks that the test file imports django settings correctly.'
        )
        parser.add_option(
            "-r",
            "--regex",
            help="write report to FILE",
        )
        (opts, files) = parser.parse_args()

        regex = r'{}'.format(opts.regex)
        if len(files) == 0:
            parser.error('No filenames provided')

        self.check_file(files, regex)
        return 1 if self.errors else 0


if __name__ == '__main__':
    checker = UpdateCommitMsg()
    sys.exit(checker.main())
