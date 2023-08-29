<template>
  <div>
    <div class="n-layout-page-header">
      <n-card :bordered="false" title="角色管理">
        角色管理，角色添加删除编辑分配权限。
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
          <n-button type="primary" @click="showAddRoleModal()">
            <template #icon>
              <n-icon>
                <PlusOutlined />
              </n-icon>
            </template>
            添加角色
          </n-button>
        </template>

        <template #action>
          <TableAction />
        </template>
      </BasicTable>
    </n-card>

    <n-modal v-model:show="showModal" :show-icon="false" preset="dialog" :title="editRoleTitle" @close="closeTreeModal">
      <n-scrollbar style="max-height: 500px" trigger="hover">
        <div class="py-3 menu-list">
          <n-tree
            ref="treeRef"
            block-line
            :cascade="iscascade"
            checkable
            :virtual-scroll="true"
            :data="treeData"
            :expandedKeys="expandedKeys"
            :checked-keys="checkedKeys"
            style="max-height: 950px; overflow: hidden"
            @update:checked-keys="checkedTree"
            @update:expanded-keys="onExpandedKeys"
          />
        </div>
      </n-scrollbar>
      <template #action>
        <n-space>
          <n-button type="info" ghost icon-placement="left" @click="packHandle">
            全部{{ expandedKeys.length ? '收起' : '展开' }}
          </n-button>

          <n-button type="info" ghost icon-placement="left" @click="checkedAllHandle">
            全部{{ checkedAll ? '取消' : '选择' }}
          </n-button>
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
            <n-form-item label="角色名称" path="role_name">
              <n-input v-model:value="formValue.role_name" placeholder="输入角色名称" />
            </n-form-item>
            <n-form-item label="是否启用" path="status">
              <n-switch v-model:value="formValue.role_status">
                <template #checked>
                  是
                </template>
                <template #unchecked>
                  否
                </template>
              </n-switch>
            </n-form-item>
            <n-form-item label="角色描述" path="role_desc">
              <n-input
                v-model:value="formValue.role_desc"
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
  import { getRoleList, updateRoleAuth, addRole, updateRole, delRole } from '@/api/system/role';
  import { getMenuList } from '@/api/system/menu';
  import { columns } from './columns';
  import { PlusOutlined } from '@vicons/antd';
  import { getTreeAll } from '@/utils';
  import { useRouter } from 'vue-router';

  const router = useRouter();
  const message = useMessage();
  const dialog = useDialog();
  const actionRef = ref();
  const treeRef = ref();
  const formRef = ref();

  const showModal = ref(false);
  const formBtnLoading = ref(false);
  const checkedAll = ref(false);
  const iscascade = ref(false);
  const editRoleTitle = ref('');
  const editRoleId = ref(0)
  const treeData = ref([]);
  const expandedKeys = ref([]);
  const checkedKeys = ref(['console', 'step-form']);

  const defaultValueRef = () => ({
    role_name: '',
    role_status: false,
    role_desc: '',
  });

  let formValue = reactive(defaultValueRef());

  const [modalRegister, { setProps, openModal, closeModal, setSubLoading }] = useModal({
        title: '新增角色',
  });

  function closeTreeModal() {
    showModal.value = false;
    iscascade.value = false;
  }

  function showAddRoleModal(isEdit = false, record) {
    if (isEdit) {
      setProps({
        title: '编辑角色',
      })
      formValue = Object.assign(unref(formValue), record);
    } else {
      setProps({
        title: '新增角色',
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
      try{
        if (!errors) {
          setSubLoading(true);
          if(formValue?.id > 0){
            const updateResult = await updateRole(formValue)
            if(updateResult){
              message.success('更新成功')
            }
          }else{
            const backRole = await addRole(formValue)
            if(backRole){
              message.success('添加成功')
            }
          }
          setSubLoading(false);
          closeModal();
          reloadTable();
        } else {
          message.error('验证失败，请填写完整信息');
        }
      }catch(e){
        setSubLoading(false);
        closeModal()
        reloadTable();
      }

    })
  }

  const rules = {
    role_name: {
      required: true,
      message: '请输入角色名称',
      trigger: 'blur',
    },
    role_desc: {
      required: true,
      message: '请输入详细描述',
      trigger: 'blur',
    },
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
            label: '角色权限',
            onClick: handleMenuAuth.bind(null, record),
            // 根据业务控制是否显示 isShow 和 auth 是并且关系
            ifShow: () => {
              return true;
            },
            // 根据权限控制是否显示: 有权限，会显示，支持多个
            auth: ['role_update_auth'],
          },
          {
            label: '编辑',
            onClick: handleEdit.bind(null, record),
            ifShow: () => {
              return true;
            },
            auth: ['role_update'],
          },
          {
            label: '删除',
            onClick: handleDelete.bind(null, record),
            // 根据业务控制是否显示 isShow 和 auth 是并且关系
            ifShow: () => {
              return true;
            },
            // 根据权限控制是否显示: 有权限，会显示，支持多个
            auth: ['role_del'],
          },
        ],
      });
    },
  });

  const loadDataTable = async (res: any) => {
    let _params = {
      ...res,
    };
    const role_list = await getRoleList(_params);
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
      const checkedId = findTreeDataId();
      const data = {
        auth_ids: checkedId,
        role_id: editRoleId.value
      }
      await updateRoleAuth(data)
      showModal.value = false;
      message.success('提交成功');
      reloadTable();
      formBtnLoading.value = false;
    } catch (error) {
      showModal.value = false;
      formBtnLoading.value = false;
      reloadTable();
    }finally{
      iscascade.value = false;
    }
  }

  function findTreeDataId() {
    const tree = treeData.value;
    const keys = checkedKeys.value;
    const checkedId = []
    keys.forEach((key)=>{
      tree.forEach((item)=>{
        if(item.key === key){
          checkedId.push(item.id)
        }else{
          if(item.children){
            item.children.forEach((child)=>{
              if(child.key === key){
                checkedId.push(child.id)
              }
            })
          }
        }
      })
    })
    return checkedId;
  }

  function handleEdit(record: Recordable) {
    showAddRoleModal(true, record)
  }

  function handleDelete(record: Recordable) {
    dialog.info({
      title: '提示',
      content: `您确定想删除此角色吗?`,
      positiveText: '确定',
      negativeText: '取消',
      onPositiveClick: async () => {
        try {
          const result = await delRole(record)
          if(result){
            message.success('删除成功');
            reloadTable();
          }
        } catch (error) {}
      },
      onNegativeClick: () => {
        message.error('已取消');
      },
    });
  }

  function handleMenuAuth(record: Recordable) {
    editRoleTitle.value = `分配 ${record.role_name} 的菜单权限`;
    editRoleId.value = record.id;
    checkedKeys.value = record.auth_keys;
    showModal.value = true;
  }

  function checkedTree(keys) {
    iscascade.value = true;
    checkedKeys.value = [...keys];
  }

  function onExpandedKeys(keys) {
    expandedKeys.value = keys;
  }

  function packHandle() {
    if (expandedKeys.value.length) {
      expandedKeys.value = [];
    } else {
      expandedKeys.value = treeData.value.map((item: any) => item.key) as [];
    }
  }

  function checkedAllHandle() {
    if (!checkedAll.value) {
      checkedKeys.value = getTreeAll(treeData.value);
      checkedAll.value = true;
    } else {
      checkedKeys.value = [];
      checkedAll.value = false;
    }
  }

  onMounted(async () => {
    const treeMenuList = await getMenuList();
    expandedKeys.value = treeMenuList.map((item) => item.key);
    treeData.value = treeMenuList;
  });
</script>

<style lang="less" scoped></style>
