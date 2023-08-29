/*
 Navicat Premium Data Transfer

 Source Server         : localhost
 Source Server Type    : MySQL
 Source Server Version : 80032
 Source Host           : localhost:3306
 Source Schema         : fast_rbac

 Target Server Type    : MySQL
 Target Server Version : 80032
 File Encoding         : 65001

 Date: 29/08/2023 11:03:02
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for access_log
-- ----------------------------
DROP TABLE IF EXISTS `access_log`;
CREATE TABLE `access_log`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `create_time` datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) COMMENT '创建时间',
  `update_time` datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6) COMMENT '更新时间',
  `user_id` int NOT NULL COMMENT '用户ID',
  `target_url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '访问的url',
  `user_agent` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '访问UA',
  `request_params` json NULL COMMENT '请求参数get|post',
  `ip` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '访问IP',
  `note` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '备注',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '用户操作记录表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of access_log
-- ----------------------------

-- ----------------------------
-- Table structure for auth
-- ----------------------------
DROP TABLE IF EXISTS `auth`;
CREATE TABLE `auth`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `create_time` datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) COMMENT '创建时间',
  `update_time` datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6) COMMENT '更新时间',
  `auth_name` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '权限名称',
  `subtitle` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '副标题',
  `pid` int NOT NULL DEFAULT 0 COMMENT '父id',
  `permission` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '权限标识',
  `auth_desc` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '权限描述',
  `is_check` tinyint(1) NOT NULL DEFAULT 0 COMMENT '是否验证权限 True为验证 False不验证',
  `auth_type` int NULL DEFAULT NULL COMMENT '0表示前端菜单权限，1表示后端接口权限',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `permission`(`permission`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 38 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '权限表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of auth
-- ----------------------------
INSERT INTO `auth` VALUES (1, '2023-08-05 11:16:14.116645', '2023-08-28 09:36:55.962317', '前端-Dashboard', '看板', 0, 'dashboard', 'Dashboard根目录', 0, 0);
INSERT INTO `auth` VALUES (2, '2023-08-05 11:16:56.614999', '2023-08-05 11:23:38.467520', '主控台', '主控台', 1, 'dashboard_console', '主控台', 1, 0);
INSERT INTO `auth` VALUES (3, '2023-08-05 11:17:29.745784', '2023-08-05 11:23:40.055493', '监控页', '监控页', 1, 'dashboard_monitor', '监控台', 1, 0);
INSERT INTO `auth` VALUES (4, '2023-08-05 11:18:25.077048', '2023-08-05 11:23:43.501083', '工作台', '工作台', 1, 'dashboard_workplace', '工作台', 1, 0);
INSERT INTO `auth` VALUES (15, '2023-08-26 11:04:36.384351', '2023-08-28 09:28:59.015052', '前端-系统设置权限', '系统设置', 0, 'system', '系统设置目录', 0, 0);
INSERT INTO `auth` VALUES (16, '2023-08-26 11:06:11.833464', '2023-08-26 11:06:27.371667', '权限管理', '权限管理', 15, 'system_auth', '权限管理', 1, 0);
INSERT INTO `auth` VALUES (17, '2023-08-26 11:06:56.183529', '2023-08-26 11:06:56.183529', '角色管理', '角色管理', 15, 'system_role', '权限管理', 1, 0);
INSERT INTO `auth` VALUES (18, '2023-08-26 11:07:31.799816', '2023-08-26 11:07:35.178370', '用户管理', '用户设置', 15, 'system_user', '用户管理', 1, 0);
INSERT INTO `auth` VALUES (19, '2023-08-26 11:08:01.819072', '2023-08-26 11:08:01.819072', '系统设置', '系统设置', 15, 'system_setting', '系统设置', 1, 0);
INSERT INTO `auth` VALUES (20, '2023-08-26 11:10:31.892381', '2023-08-26 11:10:31.892381', '隐藏页权限', '隐藏页权限', 0, 'hidden_page', '隐藏页权限', 1, 0);
INSERT INTO `auth` VALUES (21, '2023-08-28 09:27:03.040372', '2023-08-28 09:27:03.040372', '后端权限目录', '后端权限', 0, 'backend_dir', '后端权限目录', 0, 1);
INSERT INTO `auth` VALUES (22, '2023-08-28 09:30:54.738213', '2023-08-28 09:30:54.738213', '用户列表接口权限', '用户列表', 21, 'user_list', '用户列表接口权限', 1, 1);
INSERT INTO `auth` VALUES (23, '2023-08-28 09:35:46.976173', '2023-08-28 09:35:46.976173', '角色选项接口权限', '角色选项', 21, 'roles_options', '角色选项接口', 1, 1);
INSERT INTO `auth` VALUES (24, '2023-08-28 09:39:55.038270', '2023-08-28 09:39:55.038270', '用户角色更新接口权限', '用户角色更新', 21, 'update_user_role', '用户角色更新', 1, 1);
INSERT INTO `auth` VALUES (25, '2023-08-28 09:40:25.366197', '2023-08-28 09:40:25.366197', '用户添加接口权限', '用户添加', 21, 'user_add', '用户添加', 1, 1);
INSERT INTO `auth` VALUES (26, '2023-08-28 09:41:18.668068', '2023-08-28 09:41:18.668068', '用户更新接口权限', '用户更新', 21, 'user_update', '用户更新', 1, 1);
INSERT INTO `auth` VALUES (27, '2023-08-28 09:41:55.834406', '2023-08-28 09:41:55.834406', '用户删除接口权限', '用户删除', 21, 'user_del', '用户删除', 1, 1);
INSERT INTO `auth` VALUES (28, '2023-08-28 09:43:20.411436', '2023-08-28 09:43:20.411436', '角色列表接口权限', '角色列表接口', 21, 'role_list', '角色列表', 1, 1);
INSERT INTO `auth` VALUES (29, '2023-08-28 09:44:00.693561', '2023-08-28 09:44:00.693561', '角色权限分配接口权限', '角色权限分配', 21, 'role_update_auth', '角色权限分配', 1, 1);
INSERT INTO `auth` VALUES (30, '2023-08-28 10:23:06.180479', '2023-08-28 10:23:16.227451', '角色添加接口权限', '角色添加接口', 21, 'role_add', '角色添加', 1, 1);
INSERT INTO `auth` VALUES (31, '2023-08-28 10:23:46.458861', '2023-08-28 10:24:24.676944', '角色更新接口权限', '更新角色接口', 21, 'role_update', '更新角色', 1, 1);
INSERT INTO `auth` VALUES (32, '2023-08-28 10:24:13.755480', '2023-08-28 10:24:29.114590', '角色删除接口权限', '删除角色接口', 21, 'role_del', '删除角色', 1, 1);
INSERT INTO `auth` VALUES (33, '2023-08-28 10:25:23.770994', '2023-08-28 10:25:23.770994', '权限列表接口', '权限列表', 21, 'auth_list', '权限列表', 1, 1);
INSERT INTO `auth` VALUES (34, '2023-08-28 10:25:47.988880', '2023-08-28 10:26:43.755131', '权限添加接口', '添加权限', 21, 'auth_add', '添加权限', 1, 1);
INSERT INTO `auth` VALUES (35, '2023-08-28 10:26:36.373541', '2023-08-28 10:26:36.373541', '权限删除接口', '权限', 21, 'auth_del', '权限删除', 1, 1);
INSERT INTO `auth` VALUES (36, '2023-08-28 10:27:20.260270', '2023-08-28 10:27:20.260270', '权限修改接口', '权限', 21, 'auth_update', '权限修改', 1, 1);
INSERT INTO `auth` VALUES (37, '2023-08-28 21:10:31.213579', '2023-08-28 21:10:31.213579', '用户重置密码接口', '重置密码', 21, 'user_up_pwd', '重置密码', 1, 1);
INSERT INTO `auth` VALUES (40, '2023-08-28 22:11:08.624722', '2023-08-28 22:11:08.624722', '测试', '测试', 20, 'ceshi', '测试', 0, 1);
INSERT INTO `auth` VALUES (41, '2023-08-29 09:38:34.598696', '2023-08-29 09:38:34.598696', '个人信息设置接口权限', '个人信息设置', 21, 'update_profile', '个人信息设置', 1, 1);

-- ----------------------------
-- Table structure for role
-- ----------------------------
DROP TABLE IF EXISTS `role`;
CREATE TABLE `role`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `create_time` datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) COMMENT '创建时间',
  `update_time` datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6) COMMENT '更新时间',
  `role_name` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '角色名称',
  `role_status` tinyint(1) NOT NULL DEFAULT 0 COMMENT 'True:启用 False:禁用',
  `role_desc` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '角色描述',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 5 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '角色表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of role
-- ----------------------------
INSERT INTO `role` VALUES (1, '2023-08-05 11:10:33.563635', '2023-08-05 11:10:33.563635', '超级管理员', 1, '所有权限');
INSERT INTO `role` VALUES (2, '2023-08-22 09:27:29.481846', '2023-08-27 16:31:30.814010', '普通用户', 1, '用户默认角色权限');
INSERT INTO `role` VALUES (4, '2023-08-26 19:17:26.575026', '2023-08-28 11:19:23.332416', '测试角色', 1, '测试');

-- ----------------------------
-- Table structure for role_auth
-- ----------------------------
DROP TABLE IF EXISTS `role_auth`;
CREATE TABLE `role_auth`  (
  `role_id` int NOT NULL,
  `auth_id` int NOT NULL,
  INDEX `role_id`(`role_id`) USING BTREE,
  INDEX `auth_id`(`auth_id`) USING BTREE,
  CONSTRAINT `role_auth_ibfk_1` FOREIGN KEY (`role_id`) REFERENCES `role` (`id`) ON DELETE CASCADE ON UPDATE RESTRICT,
  CONSTRAINT `role_auth_ibfk_2` FOREIGN KEY (`auth_id`) REFERENCES `auth` (`id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of role_auth
-- ----------------------------
INSERT INTO `role_auth` VALUES (1, 1);
INSERT INTO `role_auth` VALUES (1, 2);
INSERT INTO `role_auth` VALUES (1, 3);
INSERT INTO `role_auth` VALUES (1, 4);
INSERT INTO `role_auth` VALUES (1, 15);
INSERT INTO `role_auth` VALUES (1, 16);
INSERT INTO `role_auth` VALUES (1, 17);
INSERT INTO `role_auth` VALUES (1, 18);
INSERT INTO `role_auth` VALUES (1, 19);
INSERT INTO `role_auth` VALUES (1, 20);
INSERT INTO `role_auth` VALUES (1, 21);
INSERT INTO `role_auth` VALUES (1, 22);
INSERT INTO `role_auth` VALUES (1, 23);
INSERT INTO `role_auth` VALUES (1, 24);
INSERT INTO `role_auth` VALUES (1, 25);
INSERT INTO `role_auth` VALUES (1, 26);
INSERT INTO `role_auth` VALUES (1, 27);
INSERT INTO `role_auth` VALUES (1, 28);
INSERT INTO `role_auth` VALUES (1, 29);
INSERT INTO `role_auth` VALUES (1, 30);
INSERT INTO `role_auth` VALUES (1, 31);
INSERT INTO `role_auth` VALUES (1, 32);
INSERT INTO `role_auth` VALUES (1, 33);
INSERT INTO `role_auth` VALUES (1, 34);
INSERT INTO `role_auth` VALUES (1, 35);
INSERT INTO `role_auth` VALUES (1, 36);
INSERT INTO `role_auth` VALUES (1, 37);
INSERT INTO `role_auth` VALUES (1, 40);
INSERT INTO `role_auth` VALUES (1, 41);
INSERT INTO `role_auth` VALUES (2, 1);
INSERT INTO `role_auth` VALUES (2, 2);
INSERT INTO `role_auth` VALUES (2, 3);
INSERT INTO `role_auth` VALUES (2, 4);
INSERT INTO `role_auth` VALUES (2, 15);
INSERT INTO `role_auth` VALUES (2, 16);
INSERT INTO `role_auth` VALUES (2, 17);
INSERT INTO `role_auth` VALUES (2, 18);
INSERT INTO `role_auth` VALUES (2, 19);
INSERT INTO `role_auth` VALUES (2, 41);

-- ----------------------------
-- Table structure for role_user
-- ----------------------------
DROP TABLE IF EXISTS `role_user`;
CREATE TABLE `role_user`  (
  `role_id` int NOT NULL,
  `user_id` int NOT NULL,
  INDEX `role_id`(`role_id`) USING BTREE,
  INDEX `user_id`(`user_id`) USING BTREE,
  CONSTRAINT `role_user_ibfk_1` FOREIGN KEY (`role_id`) REFERENCES `role` (`id`) ON DELETE CASCADE ON UPDATE RESTRICT,
  CONSTRAINT `role_user_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of role_user
-- ----------------------------
INSERT INTO `role_user` VALUES (1, 1);
INSERT INTO `role_user` VALUES (2, 2);
INSERT INTO `role_user` VALUES (2, 4);

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `create_time` datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) COMMENT '创建时间',
  `update_time` datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6) COMMENT '更新时间',
  `username` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '用户名',
  `user_type` tinyint(1) NOT NULL DEFAULT 0 COMMENT '用户类型 True:超级管理员 False:普通管理员',
  `password` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `nickname` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT 'nickname' COMMENT '昵称',
  `user_phone` varchar(11) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '手机号',
  `user_email` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '邮箱',
  `full_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '姓名',
  `user_status` int NOT NULL DEFAULT 1 COMMENT '0未激活 1正常 2禁用',
  `avatar` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '头像',
  `sex` int NULL DEFAULT 0 COMMENT '0未知 1男 2女',
  `desc` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '备注',
  `client_host` varchar(19) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '访问IP',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 5 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '用户表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of user
-- ----------------------------
INSERT INTO `user` VALUES (1, '2023-08-05 10:25:11.000000', '2023-08-29 09:57:30.595698', 'super_admin', 0, '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92', '超级管理员', '13665504672', '2878725498@qq.com', '超级管理员', 1, NULL, 0, NULL, NULL);
INSERT INTO `user` VALUES (2, '2023-08-25 19:42:53.004505', '2023-08-27 14:07:31.620866', 'ceshi', 0, '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92', '测试1号', '15255028855', '1366655@136.com', '小伙子', 0, NULL, 1, '测试小朋友', NULL);
INSERT INTO `user` VALUES (4, '2023-08-27 16:38:43.021544', '2023-08-29 00:55:21.975270', 'C02767', 1, '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92', '李逸凡', '13665504672', '2878725498@qq.com', '李逸凡', 1, NULL, 1, '系统作者', NULL);

SET FOREIGN_KEY_CHECKS = 1;
