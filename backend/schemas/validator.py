# -*- coding:utf-8 -*-
"""
@Time : 2023/8/27 13:25
@Author: 李逸凡
@Des: 
"""
import re


def strip_validator(value):
    if isinstance(value, str):
        value = value.strip()
    return value


def full_name_validator(value):
    if value is None or value == '':
        return True
    pattern = r'^[\u4E00-\u9FFF]{1,5}$'
    if isinstance(value, str):
        if re.match(pattern, value):
            return True
        else:
            return False


def phone_validator(value):
    if value is None or value == '':
        return True
    pattern = r'0?(13|14|15|18|17)[0-9]{9}'
    if isinstance(value, str):
        if re.match(pattern, value):
            return True
        else:
            return False


def email_validator(value):
    if value is None or value == '':
        return True
    pattern = r'\w[-\w.+]*@([A-Za-z0-9][-A-Za-z0-9]+\.)+[A-Za-z]{2,14}'
    if isinstance(value, str):
        if re.match(pattern, value):
            return True
        else:
            return False
