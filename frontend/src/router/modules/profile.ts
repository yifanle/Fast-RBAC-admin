import { RouteRecordRaw } from 'vue-router';
import { Layout } from '@/router/constant';
import { renderIcon } from '@/utils';
import { ProjectOutlined } from '@vicons/antd';




const routes: Array<RouteRecordRaw> = [
  {
    path: '/profile',
    name: 'Profile',
    component: Layout,
    meta: {
      sort: 100,
      title: '个人设置',
      icon: renderIcon(ProjectOutlined),
      hidden: true,
      isRoot: true,
    },
    children: [
      {
        path: 'account',
        name: 'setting-account',
        meta: {
          title: '个人设置',
        },
        component: () => import('@/views/setting/account/account.vue'),
      },
    ],
  },
];

export default routes;
