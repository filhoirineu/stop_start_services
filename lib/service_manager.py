import win32serviceutil
import wmi
from time import sleep
import os
import subprocess

WAITING = 20


class ServiceManager():
    def __init__(self, service_name, process_name):

        self.service_name = service_name
        self.process_name = process_name

        self.service_status = 0
        self.service_status_description = ""

        self.is_online = False
        self.is_disabled = False

        self.query_status = None
        self.query_startup_type = None

        self.default_service_status_description = {
            "1": "SERVICE_STOPPED",
            "2": "SERVICE_START_PENDING",
            "3": "SERVICE_STOP_PENDING",
            "4": "SERVICE_RUNNING",
            "5": "SERVICE_CONTINUE_PENDING",
            "6": "SERVICE_PAUSE_PENDING",
            "7": "SERVICE_PAUSED",
        }

        self.set_service_status()
        self.set_service_startup_type()

    def start_service(self):
        if not self.is_disabled and not self.is_online:
            verifies = 0
            win32serviceutil.StartService(serviceName=self.service_name)
            self.set_service_status()

            while not self.service_status == 4:
                self.set_service_status()
                if verifies <= WAITING:
                    sleep(0.5)
                    verifies += 1
                else:
                    self.is_online = False
                    break

    def stop_service(self):
        verifies = 0
        self.set_service_status()

        if self.is_online:
            win32serviceutil.StopService(serviceName=self.service_name)

            while self.is_online:
                if verifies <= WAITING:
                    sleep(0.5)
                    verifies += 1
                else:
                    self.kill_process()
                    break

                self.set_service_status()

            self.is_online = False

    def restart_service(self):
        self.stop_service()
        self.start_service()

    def kill_process(self):
        verifies = 0
        self.set_service_status()
        if self.is_online:
            kill_command = 'taskkill /IM ' + self.process_name + ' /F'
            subprocess.call(
                kill_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.set_service_status()
            while self.is_online:
                if verifies <= WAITING:
                    sleep(0.5)
                    verifies += 1
                    self.set_service_status()

    def set_service_status(self):
        self.query_status = win32serviceutil.QueryServiceStatus(
            serviceName=self.service_name)
        self.service_status = self.query_status[1]
        try:
            self.service_status_description = self.default_service_status_description[str(
                self.service_status)]
        except:
            self.service_status_description = ""

        self.is_online = self.service_status != 1

    def set_service_startup_type(self):
        c = wmi.WMI()
        local = c.Win32_Service(Name=self.service_name.upper())
        if len(local) > 0:
            self.is_disabled = local[0].StartMode.upper() == "DISABLED"
        else:
            self.is_disabled = True
