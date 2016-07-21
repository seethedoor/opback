# -*- coding:utf-8 -*-
# !/usr/bin/env python
#
# Author: Shawn.T
# Email: shawntai.ds@gmail.com
#
# This is the init file for the walker package
# holding api & urls of the user module
#
from .shellWalker import ShellWalkerAPI
from .scriptWalker import ScriptAPI, ScriptWalkerAPI
# , PbWalkerAPI, ScriptWalkerAPI
from .. import api

api.add_resource(
    ShellWalkerAPI, '/api/v0.0/shellwalker', endpoint='shellwalker_ep')
api.add_resource(
    ScriptAPI, '/api/v0.0/script', endpoint='script_ep')
# api.add_resource(
#     PbWalkerAPI, '/api/v0.0/pbwalker', endpoint='pbwalker_ep')
api.add_resource(
    ScriptWalkerAPI, '/api/v0.0/scriptwalker', endpoint='scriptwalker')
