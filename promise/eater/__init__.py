# -*- coding:utf-8 -*-
# !/usr/bin/env python
#
# Author: Leann Mak
# Email: leannmak@139.com
#
# This is the init file defining api with urls for the eater package.
#

from .services import HostListAPI, HostAPI, \
    HostGroupListAPI, HostGroupAPI, HostSyncAPI
from .. import api

"""
    Data Services
"""
api.add_resource(
    HostListAPI, '/api/v0.0/eater/host', endpoint='et_host_list_ep')
api.add_resource(
    HostAPI, '/api/v0.0/eater/host/<id>', endpoint='et_host_id_ep')
api.add_resource(
    HostGroupListAPI, '/api/v0.0/eater/hostgroup',
    endpoint='et_hostgroup_list_ep')
api.add_resource(
    HostGroupAPI, '/api/v0.0/eater/hostgroup/<id>',
    endpoint='et_hostgroup_id_ep')

"""
    Task Services
"""
api.add_resource(
    HostSyncAPI, '/api/v0.0/eater/hostsync', endpoint='et_host_sync_ep')
api.add_resource(
    HostSyncAPI, '/api/v0.0/eater/hostsync/<id>',
    endpoint='et_host_sync_id_ep')
