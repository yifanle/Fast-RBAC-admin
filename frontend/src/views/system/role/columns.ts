import { h } from 'vue';
import { NTag } from 'naive-ui';

export const columns = [
  {
    title: 'id',
    key: 'id',
  },
  {
    title: '角色名称',
    key: 'role_name',
  },
  {
    title: '角色描述',
    key: 'role_desc',
  },
  {
    title: '启用状态',
    key: 'role_status',
    render(row) {
      return h(
        NTag,
        {
          type: row.role_status ? 'success' : 'error',
        },
        {
          default: () => (row.role_status ? '启用' : '停用'),
        }
      );
    },
  },
  {
    title: '创建时间',
    key: 'create_time',
  },
];
