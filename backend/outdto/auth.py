# -*- coding:utf-8 -*-
"""
@Time : 2023/8/8 22:58
@Author: 李逸凡
@Des: 
"""

from models.base import Auth


class AuthInfo:

    def __init__(self, auth: Auth):
        self.id = auth.pk
        self.pid = auth.pid
        self.label = auth.auth_name
        self.key = auth.permission
        self.subtitle = auth.subtitle
        self.auth = auth.permission
        self.type = auth.auth_type
        self.desc = auth.auth_desc
        self.is_check = auth.is_check
        self.children = []
