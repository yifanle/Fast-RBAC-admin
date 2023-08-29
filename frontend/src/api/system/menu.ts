import { http } from '@/utils/http/axios';

/**
 * @description: 根据用户id获取用户菜单
 */
export function adminMenus() {
  return http.request({
    url: '/menus',
    method: 'GET',
  });
}

/**
 * 获取tree菜单列表
 * @param params
 */
export function getMenuList() {
  return http.request({
    url: '/admin/user_auth/list',
    method: 'GET',
  });
}

/**
 * 更新菜单
 * @returns
 */
export function updateMenu(params) {
  return http.request({
    url: '/admin/user_auth/update',
    method: 'POST',
    params
  });
}

/**
 * 添加菜单
 * @returns
 */
export function addMenu(params) {
  return http.request({
    url: '/admin/user_auth/add',
    method: 'POST',
    params
  });
}

/**
 * 删除菜单
 * @returns
 */
export function delMenu(params) {
  return http.request({
    url: '/admin/user_auth/del?auth_id='+params,
    method: 'DELETE',
  });
}

