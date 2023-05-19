# -*- coding: utf-8 -*-
import datetime
import requests
import logging
import json
from datetime import datetime

from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)
odoo_session = requests.Session()


# class ZhaoguWeb(http.Controller):
