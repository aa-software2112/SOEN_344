from . import controllers
from flask import Flask, request, jsonify, make_response

from uber_sante.utils import json_helper as js
from uber_sante.utils import cookie_helper
from uber_sante.utils.cache import get_from_cache, set_to_cache

from uber_sante.services.nurse_service import NurseService

nurse_service = NurseService()
