import { http } from '@/utils/http/axios';

export interface BasicResponseModel<T = any> {
  code: number;
  message: string;
  result: T;
}

export interface BasicPageParams {
  pageNumber: number;
  pageSize: number;
  total: number;
}

/**
 * @description: 获取用户信息
 */
export function getUserInfo() {
  return http.request({
    url: '/admin/user/info',
    method: 'get',
  });
}

/**
 * @description: 用户登录
 */
export function login(params) {
  return http.request<BasicResponseModel>(
    {
      url: '/admin/user/login',
      method: 'POST',
      params,
    },
    {
      isTransformResponse: false,
    }
  );
}

/**
 * @description: 用户修改密码
 */
export function changePassword(params, uid) {
  return http.request(
    {
      url: `/user/u${uid}/changepw`,
      method: 'POST',
      params,
    },
    {
      isTransformResponse: false,
    }
  );
}

/**
 * @description: 用户登出
 */
export function logout(params) {
  return http.request({
    url: '/login/logout',
    method: 'POST',
    params,
  });
}

/**
 * @description: 角色列表
 */
export function getUserList(params) {
  return http.request({
    url: '/admin/user/page',
    method: 'POST',
    params,
  });
}

/**
 * @description: 更新用户角色
 */
export function updateUserRoles(params) {
  return http.request({
    url: '/admin/user/update_user_role',
    method: 'POST',
    params,
  });
}


/**
 * @description: 创建用户
 */
export function createUser(params) {
  return http.request({
    url: '/admin/user/add',
    method: 'POST',
    params,
  });
}

/**
 * @description: 创建用户
 */
export function updateUser(params) {
  return http.request({
    url: '/admin/user/update',
    method: 'POST',
    params,
  });
}


/**
 * @description: 删除用户
 */
export function delUser(id) {
  return http.request({
    url: '/admin/user/del?user_id=' + id,
    method: 'DELETE',
  });
}

/**
 * @description: 重置密码
 */
export function resetPwd(id) {
  return http.request({
    url: '/admin/user/reset_pwd?user_id=' + id,
    method: 'GET',
  });
}

/**
 * @description: 个人设置
 */
export function updateAccount(params) {
  return http.request({
    url: '/admin/user/profile/account',
    method: 'POST',
    params
  });
}

/**
 * @description: 个人设置
 */
export function updatePwd(params) {
  return http.request({
    url: '/admin/user/profile/pwd_modify',
    method: 'POST',
    params
  });
}