#-*- coding:utf-8 -*-
#
# Copyright © 2016–2017 Liang Feng <finalion@gmail.com>
#
# Support: Report an issue at https://github.com/finalion/WordQuery/issues
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version; http://www.gnu.org/copyleft/gpl.html.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import inspect
import os
from functools import wraps

from aqt import mw
from aqt.qt import QThread
from aqt.utils import showInfo
from .base import LocalService, MdxService, StardictService, WebService
from ..context import config
from ..utils import MapDict, importlib


class ServiceManager(object):

    def __init__(self):
        self.update_services()

    @property
    def services(self):
        return self.web_services | self.local_services

    # def start_all(self):
    #     self.fetch_headers()
        # make all local services available
        # for service in self.local_services:
        #     if not service.index(only_header=True):
        #         self.local_services.remove(service)

    def update_services(self):
        self.web_services, self.local_custom_services = self._get_services_from_files()
        self.local_services = self._get_available_local_services()
        # self.fetch_headers()
        # combine the customized local services into local services
        self.local_services.update(self.local_custom_services)

    def get_service(self, unique):
        # webservice unique: class name
        # mdxservice unique: dict filepath
        for each in self.services:
            if each.unique == unique:
                return each

    def get_service_action(self, service, label):
        for each in service.fields:
            if each.label == label:
                return each

    def _get_services_from_files(self, *args):
        """
        get service from service packages, available type is
        WebService, LocalService
        """
        web_services, local_custom_services = set(), set()
        mypath = os.path.dirname(os.path.realpath(__file__))
        files = [f for f in os.listdir(mypath)
                 if f not in ('__init__.py', 'base.py', 'manager.py') and not f.endswith('.pyc')]
        base_class = (WebService, LocalService,
                      MdxService, StardictService)

        for f in files:
            try:
                module = importlib.import_module(
                    '.%s' % os.path.splitext(f)[0], __package__)
                for name, cls in inspect.getmembers(module, predicate=inspect.isclass):
                    if cls in base_class:
                        continue
                    try:
                        service = cls(*args)
                        if issubclass(cls, WebService):
                            web_services.add(service)
                         # get the customized local services
                        if issubclass(cls, LocalService):
                            local_custom_services.add(service)
                    except Exception:
                        # exclude the local service whose path has error.
                        pass
            except ImportError:
                continue
        return web_services, local_custom_services

    def _get_available_local_services(self):
        services = set()
        for each in config.dirs:
            for dirpath, dirnames, filenames in os.walk(each):
                for filename in filenames:
                    dict_path = os.path.join(dirpath, filename)
                    if MdxService.support(dict_path):
                        services.add(MdxService(dict_path))
                    if StardictService.support(dict_path):
                        services.add(StardictService(dict_path))
                # support mdx dictionary and stardict format dictionary
        return services
