#  Copyright (c) JAAK-IT SAPI DE CV - All Rights Reserved - 2022
#  Unauthorized copying of this file, via any medium is strictly prohibited
#  Proprietary and confidential
#  Written by Mauricio Portugués <mauricio.portugues@jaak-it.com>
#  Support <support@jaak-it.com>

#!/usr/bin/python

from datadog_checks.base import AgentCheck
import os
import subprocess

class SupervisorCheck(AgentCheck):
    def check(self, instance):
        CMD = "sudo supervisorctl status | awk '/RUNNING/ {print $1,$2}'"
        supervisor_output = subprocess.check_output(CMD, shell=True).decode("utf-8").split('\n')

        for supervisor_line in supervisor_output:
            if supervisor_line != '':
                if 'RUNNING' in supervisor_line:
                    print(supervisor_line + ':\tVERDADERO')
                    self.gauge("supervisor.processes", 1, tags=['SUPERVISOR_STATUS:OK'] + self.instance.get('tags', []))
                else:
                    self.gauge("supervisor.processes", 0, tags=['SUPERVISOR_STATUS:ERROR'] + self.instance.get('tags', []))
                    os.popen('sudo supervisorctl restart ' + supervisor_line.split(' ')[0])
