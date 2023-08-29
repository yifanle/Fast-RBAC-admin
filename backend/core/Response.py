# -*- coding:utf-8 -*-
"""
@Time : 2022/4/24 10:11 AM
@Author: binkuolo
@Des: 常用返回类型封装
"""
from enum import Enum
from typing import List


def res_antd(data: List = None, total: int = 0, code: bool = True):
    """
    支持ant-design-table 返回的格式
    :param code:
    :param data:
    :param total:
    :return:
    """
    if data is None:
        data = []
    result = {
        "success": code,
        "data": data,
        "total": total
    }
    return result


def base_response(code, msg, result_type, data=None):
    """基础返回格式"""
    if data is None:
        data = []
    result = {
        "code": code,
        "message": msg,
        "result": data,
        "type": result_type
    }
    return result


def success(data=True, msg=''):
    """成功返回格式"""
    if data is None:
        data = True
    return base_response(200, msg, 'success', data)


def fail(msg='', data=False):
    """失败返回格式"""
    if data is None:
        data = False
    return base_response(-1, msg, 'error', data)


class ResponseCode(Enum):
    # users
    USER_QUERY_NOT_FOUND = 10000
    USER_NOT_FOUND = 10001
    PWD_MODIFY_FAIL = 10002
    PWD_INCORRECT_ERROR = 10003
    USER_BANED_ERROR = 10004
    UPDATE_USER_ROLES_ERROR = 10005
    USER_EXIST_ERROR = 10006
    USER_CREATE_FAIL = 10007
    USER_UPDATE_FAIL = 10008
    USER_DELETE_FAIL = 10009
    USER_OLD_PASSWORD_INCORRECT = 10010
    USER_PWD_OLD_NEW_SAME = 10011
    # roles
    ROLE_QUERY_NOT_FOUND = 20000
    ROLE_NOT_FOUND = 20001
    ROLE_EXIST_ERROR = 20002
    ROLE_CREATE_FAIL = 20003
    CHANGE_DEFAULT_ROLE_NAME_ERROR = 20004
    ROLE_UPDATE_FAIL = 20005
    DELETE_DEFAULT_ROLE_ERROR = 20006
    ROLE_DELETE_FAIL = 20007
    # auth
    AUTH_QUERY_NOT_FOUND = 30000
    AUTH_NOT_FOUND = 30001
    AUTH_CREATE_FAIL = 30002
    AUTH_EXIST_ERROR = 30003
    AUTH_UPDATE_FAIL = 30004
    AUTH_DELETE_FAIL = 30005
    AUTH_TREE_CHILD_EXIST = 30006
    # success
    SUCCESS_CODE = 200


class MiddleResponse:
    def __init__(self, code: ResponseCode, data=None):
        self.code = code
        self.data = data


def response_code_handler(m: MiddleResponse):
    code_msg_map = {
        # user
        ResponseCode.USER_QUERY_NOT_FOUND: "用户查询失败",
        ResponseCode.USER_NOT_FOUND: "用户不存在",
        ResponseCode.PWD_INCORRECT_ERROR: "用户名或密码不正确",
        ResponseCode.PWD_MODIFY_FAIL: "密码修改失败",
        ResponseCode.USER_BANED_ERROR: "该用户已被禁用或未激活，请联系管理员",
        ResponseCode.UPDATE_USER_ROLES_ERROR: "修改用户角色失败",
        ResponseCode.USER_EXIST_ERROR: "用户名已存在",
        ResponseCode.USER_CREATE_FAIL: "创建用户失败",
        ResponseCode.USER_UPDATE_FAIL: "修改用户信息失败",
        ResponseCode.USER_DELETE_FAIL: "删除用户失败",
        ResponseCode.USER_OLD_PASSWORD_INCORRECT: "密码修改失败，原密码不正确",
        ResponseCode.USER_PWD_OLD_NEW_SAME: "密码修改失败，新密码和原密码相同",
        # role
        ResponseCode.ROLE_QUERY_NOT_FOUND: "角色查询失败",
        ResponseCode.ROLE_NOT_FOUND: "角色不存在",
        ResponseCode.ROLE_EXIST_ERROR: "角色已存在",
        ResponseCode.ROLE_CREATE_FAIL: "角色创建失败",
        ResponseCode.CHANGE_DEFAULT_ROLE_NAME_ERROR: "默认角色名称无法修改",
        ResponseCode.ROLE_UPDATE_FAIL: "修改角色信息失败",
        ResponseCode.DELETE_DEFAULT_ROLE_ERROR: "默认角色名称无法删除",
        ResponseCode.ROLE_DELETE_FAIL: "删除角色失败",
        # auth
        ResponseCode.AUTH_QUERY_NOT_FOUND: "权限查询失败",
        ResponseCode.AUTH_NOT_FOUND: "目标权限不存在",
        ResponseCode.AUTH_CREATE_FAIL: "权限创建失败",
        ResponseCode.AUTH_EXIST_ERROR: "已存在该权限,权限或标签名重复",
        ResponseCode.AUTH_UPDATE_FAIL: "修改权限失败",
        ResponseCode.AUTH_DELETE_FAIL: "删除权限失败",
        ResponseCode.AUTH_TREE_CHILD_EXIST: "该权限无法删除：存在子权限",
        # success
        ResponseCode.SUCCESS_CODE: "操作成功"
    }
    msg = code_msg_map.get(m.code, "操作失败")
    if m.code == ResponseCode.SUCCESS_CODE:
        return success(msg=msg, data=m.data)
    else:
        return fail(msg=msg, data=m.data)
