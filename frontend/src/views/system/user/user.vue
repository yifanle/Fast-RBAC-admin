<template>
  <div>
    <div class="n-layout-page-header">
      <n-card :bordered="false" title="用户管理">
        用户管理，用户添加删除编辑分配权限。

      </n-card>
    </div>
    <n-card :bordered="false" class="mt-4 proCard">
      <BasicTable
        :columns="columns"
        :request="loadDataTable"
        :row-key="(row) => row.id"
        ref="actionRef"
        :actionColumn="actionColumn"
        @update:checked-row-keys="onCheckedRow"
      >
        <template #tableTitle>
          <n-button type="primary" @click="addUserModal">
            <template #icon>
              <n-icon>
                <PlusOutlined />
              </n-icon>
            </template>
            添加用户
          </n-button>
        </template>

        <template #action>
          <TableAction />
        </template>
      </BasicTable>
    </n-card>

    <n-modal v-model:show="showModal" :show-icon="false" preset="dialog" :title="editUserTitle">
      <n-space vertical>
        <n-tag round :bordered="false" type="success">
          用户角色分配后请重新登录该用户以生效权限！
          <template #icon>
            <n-icon :component="BellTwotone" />
          </template>
        </n-tag>
        <n-transfer
          ref="transfer"
          v-model:value="roleIds"
          virtual-scroll
          :options="roleList"
          source-filterable
          target-filterable
        />
      </n-space>
      <template #action>
        <n-space>
          <n-button type="primary" :loading="formBtnLoading" @click="confirmForm">提交</n-button>
        </n-space>
      </template>
    </n-modal>
    <basicModal @register="modalRegister" ref="modalRef" class="basicModal" @on-close="resetForm" @on-ok="formSubmit">
      <template #default>
        <n-form
            :label-width="80"
            :model="formValue"
            :rules="rules"
            label-placement="left"
            ref="formRef"
            class="py-8"
          >
            <n-form-item label="用户名" path="username">
              <n-input v-model:value="formValue.username" placeholder="输入用户名" />
            </n-form-item>
            <n-form-item v-if="!isEdit" label="密码" path="password">
              <n-input type="password" v-model:value="formValue.password" placeholder="输入密码" />
            </n-form-item>
            <n-form-item v-if="!isEdit" label="确认密码" path="reenterPassword">
              <n-input type="password" v-model:value="formValue.reenterPassword" placeholder="重新输入密码" />
            </n-form-item>
            <n-form-item label="昵称" path="nickname">
              <n-input v-model:value="formValue.nickname" placeholder="输入昵称" />
            </n-form-item>
            <n-form-item label="手机号" path="user_phone">
              <n-input v-model:value="formValue.user_phone" placeholder="输入手机号" />
            </n-form-item>
            <n-form-item label="邮箱" path="user_email">
              <n-input v-model:value="formValue.user_email" placeholder="输入邮箱" />
            </n-form-item>
            <n-form-item label="姓名" path="full_name">
              <n-input v-model:value="formValue.full_name" placeholder="输入姓名" />
            </n-form-item>
            <n-form-item label="性别" path="sex">
              <n-radio-group v-model:value="formValue.sex" name="sex">
                <n-space>
                  <n-radio :value="0">未知</n-radio>
                  <n-radio :value="1">男</n-radio>
                  <n-radio :value="2">女</n-radio>
                </n-space>
              </n-radio-group>
            </n-form-item>
            <n-form-item label="是否启用" path="user_status">
              <n-radio-group v-model:value="formValue.user_status" name="user_status">
                <n-space>
                  <n-radio :value="0">未激活</n-radio>
                  <n-radio :value="1">启用</n-radio>
                  <n-radio :value="2">禁用</n-radio>
                </n-space>
              </n-radio-group>
            </n-form-item>
            <n-form-item label="用户类型" path="status">
              <n-switch v-model:value="formValue.user_type">
                <template #checked>
                  超管
                </template>
                <template #unchecked>
                  普通
                </template>
              </n-switch>
            </n-form-item>
            <n-form-item v-if="isEdit" label="角色描述" path="desc">
              <n-input
                v-model:value="formValue.desc"
                type="textarea"
                placeholder="请输入角色描述"
              />
            </n-form-item>
          </n-form>
      </template>
    </basicModal>
  </div>
</template>

<script lang="ts" setup>
  import { reactive, ref,unref, h, onMounted } from 'vue';
  import { useMessage, useDialog } from 'naive-ui';
  import { BasicTable, TableAction } from '@/components/Table';
  import { basicModal, useModal } from '@/components/Modal';
  import { getAllRoleFormat } from '@/api/system/role';
  import { getUserList, updateUserRoles, createUser, updateUser, resetPwd, delUser } from '@/api/system/user';
  import { columns } from './columns';
  import { PlusOutlined,BellTwotone } from '@vicons/antd';
  import { useRouter } from 'vue-router';
  import CryptoJS from "crypto-js";
  import { FormItemRule } from 'naive-ui/lib/form/src/interface';
  const router = useRouter();
  const message = useMessage();
  const dialog = useDialog();
  const actionRef = ref();
  const formRef = ref();
  const transfer = ref();
  const isEdit = ref(false);

  const showModal = ref(false);
  const formBtnLoading = ref(false);
  const editUserTitle = ref('');
  const editUserId = ref(0)
  const roleIds = ref([]);
  const roleList = ref([]);

  const defaultValueRef = () => ({
    username: '',
    nickname: '',
    password: '',
    reenterPassword: '',
    user_type: false,
    user_status: 0,
    user_phone: '',
    user_email: '',
    full_name: '',
    desc: '',
    sex: 0,
  });

  let formValue = reactive(defaultValueRef());

  const [modalRegister, { setProps, openModal, closeModal, setSubLoading }] = useModal({
        title: '新增用户',
  });

  function showAddUserModal(record=null) {
    if (isEdit.value) {
      setProps({
        title: '编辑用户',
      })
      formValue = Object.assign(unref(formValue), record);
    } else {
      setProps({
        title: '新增用户',
      })
      formValue = reactive(defaultValueRef());
    }
    openModal();
  }

  function resetForm() {
    formRef.value.restoreValidation();
    formValue = Object.assign(unref(formValue), defaultValueRef());
  }

  const formSubmit = ()=>{
    formRef.value.validate(async (errors) => {
      try {
        if (!errors) {
          setSubLoading(true);
          if(formValue?.id > 0){
            const updateResult = await updateUser(formValue)
            setSubLoading(false);
            if(updateResult){
              message.success('更新成功')
              reloadTable()
            }
          }else{
            formValue.password = CryptoJS.SHA256(formValue.password).toString(CryptoJS.enc.Hex)
            formValue.reenterPassword = formValue.password
            const backUser = await createUser(formValue)
            setSubLoading(false);
            if(backUser){
              message.success('添加成功')
              reloadTable()
            }
          }
          closeModal()
        } else {
          setSubLoading(false);
          message.error('验证失败，请填写完整信息');
        }
      } catch (error: any) {
        closeModal();
        reloadTable();
        setSubLoading(false);
      }
    })
  }

  function validateUsername(rule: FormItemRule, value: string): boolean{
    if(value.length>3&&value.length<20){
      return true;
    }else{
      return false;
    }
  }

  function validatePassword(rule: FormItemRule, value: string): boolean{
    return value === formValue.password;
  }

  function validateEmail(rule: FormItemRule, value: string): boolean{
    if (!value) {
        return true
    }
    const pattern = /\w[-\w.+]*@([A-Za-z0-9][-A-Za-z0-9]+\.)+[A-Za-z]{2,14}/;
    return pattern.test(value);
  }

  function validatePhone(rule: FormItemRule, value: string): boolean{
    if (!value) {
        return true
    }
    const pattern = /0?(13|14|15|18|17)[0-9]{9}/;
    return pattern.test(value);
  }

  const rules = {
    username: [
      {
        required: true,
        message: '用户名不能为空',
        trigger: 'blur',
      },
      {
        validator: validateUsername,
        message: '用户名长度在 3 到 20 个字符',
        trigger: 'input'
      }
    ],
    password: {
      required: true,
      message: '密码不能为空',
      trigger: 'blur',
    },
    reenterPassword: [
      {
        required: true,
        message: '确认密码不能为空',
        trigger: 'blur',
      },
      {
        validator: validatePassword,
        message: '两次密码输入不一致',
        trigger: 'blur'
      }
    ],
    user_email: [
      {
        validator: validateEmail,
        message: '邮箱格式不正确',
        trigger: 'blur'
      }
    ],
    user_phone: [
      {
        validator: validatePhone,
        message: '手机号码格式不正确',
        trigger: 'blur'
      }
    ],
    full_name: [
      {
        validator (rule: FormItemRule, value: string) {
          if (!value) {
            return true
          } else if (!/[\u4e00-\u9fa5]/.test(value)) {
            return new Error('姓名必须是中文')
          } else if (value.length > 5) {
            return new Error('姓名必须5个字符以内')
          }
          return true
        },
        trigger: 'blur'
      }
    ],
  };

  const actionColumn = reactive({
    width: 250,
    title: '操作',
    key: 'action',
    fixed: 'right',
    render(record) {
      return h(TableAction, {
        style: 'button',
        actions: [
          {
            label: '分配角色',
            onClick: handleMenuAuth.bind(null, record),
            // 根据业务控制是否显示 isShow 和 auth 是并且关系
            ifShow: () => {
              return true;
            },
            // 根据权限控制是否显示: 有权限，会显示，支持多个
            auth: ['update_user_role'],
          },
          {
            label: '编辑',
            onClick: handleEdit.bind(null, record),
            ifShow: () => {
              return true;
            },
            auth: ['user_update'],
          },
          {
            label: '删除',
            onClick: handleDelete.bind(null, record),
            // 根据业务控制是否显示 isShow 和 auth 是并且关系
            ifShow: () => {
              return true;
            },

            // 根据权限控制是否显示: 有权限，会显示，支持多个
            auth: ['user_del'],
          },
          {
            label: '重置',
            onClick: resetPassword.bind(null, record),
            ifShow: () => {
              return true;
            },
            auth: ['user_up_pwd'],
          },
        ],
      });
    },
  });

  const loadDataTable = async (res: any) => {
    let _params = {
      ...res,
    };
    const role_list = await getUserList(_params);
    return role_list;
  };

  function onCheckedRow(rowKeys: any[]) {
    console.log(rowKeys);
  }

  function reloadTable() {
    actionRef.value.reload();
  }

  async function confirmForm(e: any) {
    try {
      e.preventDefault();
      formBtnLoading.value = true;
      const paramData = {
        id: editUserId.value,
        roles: roleIds.value,
      };
      const result = await updateUserRoles(paramData);
      if(result){
        message.success('更新成功');
        reloadTable();
      }
    } finally {
      formBtnLoading.value = false;
      showModal.value = false;
    }

  }

  function resetPassword(record: Recordable) {
    dialog.info({
      title: '提示',
      content: `您确定要重置密码吗?`,
      positiveText: '确定',
      negativeText: '取消',
      onPositiveClick: async () => {
        try{
          const result = await resetPwd(record.id)
          if(result){
            message.success('密码重置成功');
            reloadTable();
          }
        }catch(e){
        }
      },
      onNegativeClick: () => {
        message.error('已取消');
      },
    });
  }

  function handleEdit(record: Recordable) {
    isEdit.value = true;
    showAddUserModal(record)
  }

  function addUserModal() {
    isEdit.value = false;
    showAddUserModal()
  }

  function handleDelete(record: Recordable) {
    dialog.info({
      title: '提示',
      content: `您确定想删除此角色吗?`,
      positiveText: '确定',
      negativeText: '取消',
      onPositiveClick: async () => {
        try{
          const result = await delUser(record.id)
          if(result){
            message.success('删除成功');
            reloadTable();
          }
        }catch(e){
        }
      },
      onNegativeClick: () => {
        message.error('已取消');
      },
    });
  }

  function handleMenuAuth(record: Recordable) {
    editUserTitle.value = `分配 ${record.username} 的角色信息`;
    editUserId.value = record.id;
    roleIds.value = record.roles;
    showModal.value = true;
  }

  onMounted(async () => {
    roleList.value = await getAllRoleFormat();
  });
</script>

<style lang="less" scoped></style>
