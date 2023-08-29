import { http } from '@/utils/http/axios';

/**
 * @description: 角色列表
 */
export function getRoleList(params) {
  return http.request({
    url: '/admin/role/page',
    method: 'POST',
    params,
  });
}


/**
 * @description: 角色列表
 */
export function updateRoleAuth(params) {
  return http.request({
    url: '/admin/role/update_auth',
    method: 'POST',
    params,
  });
}


/**
 * @description: 新建角色
 */
export function addRole(params) {
  return http.request({
    url: '/admin/role/add_role',
    method: 'POST',
    params,
  });
}

/**
 * @description: 更新角色
 */
export function updateRole(params) {
  return http.request({
    url: '/admin/role/update_role',
    method: 'POST',
    params,
  });
}


/**
 * @description: 删除角色
 */
export function delRole(params) {
  return http.request({
    url: '/admin/role/del_role',
    method: 'DELETE',
    params,
  });
}

/**
 * @description: 查询所有角色
 */
export function getAllRoleFormat() {
  return http.request({
    url: '/admin/role/get_roles_options',
    method: 'GET',
  });
}