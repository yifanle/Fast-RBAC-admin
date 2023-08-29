import { RouteRecordRaw } from 'vue-router';
import { Layout, ParentLayout } from '@/router/constant';
import { renderIcon, renderNew } from '@/utils';
import { ProjectOutlined } from '@vicons/antd';


const IFrame = () => import('@/views/iframe/index.vue');

const routeName = 'comp';

const routes: Array<RouteRecordRaw> = [
  {
    path: '/hidden',
    name: 'Hidden',
    component: Layout,
    meta: {
      sort: 100,
      title: '隐藏菜单',
      icon: renderIcon(ProjectOutlined),
      // hidden: true,
      isRoot: true,
      permissions: ['hidden_page'], // 没有权限后不会显示在菜单栏中，也不可以通过路由访问

    },
    children: [
      {
        path: 'about',
        name: `about_index`,
        meta: {
          title: '关于项目',
          activeMenu: 'about_index',
        },
        component: () => import('@/views/about/index.vue'),
      },
      {
        path: 'directive',
        name: `directive_index`,
        meta: {
          title: '指令示例',
          activeMenu: 'directive_index',
        },
        component: () => import('@/views/directive/index.vue'),
      },
      {
        path: 'naive',
        name: 'frame-naive',
        meta: {
          title: 'NaiveUi(内嵌)',
          frameSrc: 'https://www.naiveadmin.com',
        },
        component: IFrame,
      },
      {
        path: 'success',
        name: 'result-success',
        meta: {
          title: '成功页',
        },
        component: () => import('@/views/result/success.vue'),
      },
      {
        path: 'fail',
        name: 'result-fail',
        meta: {
          title: '失败页',
        },
        component: () => import('@/views/result/fail.vue'),
      },
      {
        path: 'info',
        name: 'result-info',
        meta: {
          title: '信息页',
        },
        component: () => import('@/views/result/info.vue'),
      },
      {
        path: '403',
        name: 'exception-403',
        meta: {
          title: '403',
        },
        component: () => import('@/views/exception/403.vue'),
      },
      {
        path: '404',
        name: 'exception-404',
        meta: {
          title: '404',
        },
        component: () => import('@/views/exception/404.vue'),
      },
      {
        path: '500',
        name: 'exception-500',
        meta: {
          title: '500',
        },
        component: () => import('@/views/exception/500.vue'),
      },
      {
        path: 'basic-form',
        name: 'form-basic-form',
        meta: {
          title: '基础表单',
        },
        component: () => import('@/views/form/basicForm/index.vue'),
      },
      {
        path: 'step-form',
        name: 'form-step-form',
        meta: {
          title: '分步表单',
        },
        component: () => import('@/views/form/stepForm/stepForm.vue'),
      },
      {
        path: 'detail',
        name: 'form-detail',
        meta: {
          title: '表单详情',
        },
        component: () => import('@/views/form/detail/index.vue'),
      },
      {
        path: 'basic-list',
        name: 'basic-list',
        meta: {
          title: '基础列表',
        },
        component: () => import('@/views/list/basicList/index.vue'),
      },
      {
        path: 'basic-info/:id?',
        name: 'basic-info',
        meta: {
          title: '基础详情',
          hidden: true,
          activeMenu: 'basic-list',
        },
        component: () => import('@/views/list/basicList/info.vue'),
      },
      {
        path: 'table',
        name: `${routeName}_table`,
        redirect: '/comp/table/basic',
        component: ParentLayout,
        meta: {
          title: '表格',
        },
        children: [
          {
            path: 'basic',
            name: `${routeName}_table_basic`,
            meta: {
              title: '基础表格',
            },
            component: () => import('@/views/comp/table/basic.vue'),
          },
          {
            path: 'editCell',
            name: `${routeName}_table_editCell`,
            meta: {
              title: '单元格编辑',
            },
            component: () => import('@/views/comp/table/editCell.vue'),
          },
          {
            path: 'editRow',
            name: `${routeName}_table_editRow`,
            meta: {
              title: '整行编辑',
            },
            component: () => import('@/views/comp/table/editRow.vue'),
          },
        ],
      },
      {
        path: 'form',
        name: `${routeName}_form`,
        redirect: '/comp/form/basic',
        component: ParentLayout,
        meta: {
          title: '表单',
        },
        children: [
          {
            path: 'basic',
            name: `${routeName}_form_basic`,
            meta: {
              title: '基础使用',
            },
            component: () => import('@/views/comp/form/basic.vue'),
          },
          {
            path: 'useForm',
            name: `useForm`,
            meta: {
              title: 'useForm',
            },
            component: () => import('@/views/comp/form/useForm.vue'),
          },
        ],
      },
      {
        path: 'upload',
        name: `${routeName}_upload`,
        meta: {
          title: '上传图片',
        },
        component: () => import('@/views/comp/upload/index.vue'),
      },
      {
        path: 'modal',
        name: `${routeName}_modal`,
        meta: {
          title: '弹窗扩展',
        },
        component: () => import('@/views/comp/modal/index.vue'),
      },
      {
        path: 'richtext',
        name: `richtext`,
        meta: {
          title: '富文本',
          extra: renderNew(),
        },
        component: () => import('@/views/comp/richtext/vue-quill.vue'),
      },
      {
        path: 'drag',
        name: `Drag`,
        meta: {
          title: '拖拽',
          extra: renderNew(),
        },
        component: () => import('@/views/comp/drag/index.vue'),
      },
    ],
  },
];

export default routes;
