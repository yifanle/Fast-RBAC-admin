import { h } from 'vue';
import { NTag } from 'naive-ui';

export const columns = [
  {
    title: 'id',
    key: 'id',
  },
  {
    title: '登录名',
    key: 'username',
  },
  {
    title: '昵称',
    key: 'nickname',
  },
  {
    title: '名字',
    key: 'full_name',
  },
  {
    title: '手机号',
    key: 'user_phone',
  },
  {
    title: '邮箱',
    key: 'user_email',
  },
  {
    title: '用户类型',
    key: 'user_type',
    render(row) {
      return h(
        NTag,
        {
          type: row.user_type ? 'success' : 'warning',
        },
        {
          default: () => (row.user_type ? '超管' : '普通用户'),
        }
      );
    },
  },
  {
    title: '启用状态',
    key: 'user_status',
    render(row) {
      return h(
        NTag,
        {
          type: row.user_status===0?'warning':row.user_status===1?'success':'error',
        },
        {
          default: () => {
            const code = row.user_status;
            if(code===0){
              return '未激活';
            }else if(code===1){
              return '启用';
            }else if(code===2){
              return '禁用';
            }
          },
        }
      );
    },
  },
  {
    title: '创建时间',
    key: 'create_time',
  },
];
