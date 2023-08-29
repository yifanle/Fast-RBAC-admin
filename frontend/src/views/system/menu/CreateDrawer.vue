<template>
  <n-drawer v-model:show="isDrawer" :width="width" :placement="placement">
    <n-drawer-content :title="title" closable>
      <n-form
        :model="formParams"
        :rules="rules"
        ref="formRef"
        label-placement="left"
        :label-width="100"
      >
        <n-form-item label="类型" path="type">
          <n-radio-group v-model:value="formParams.auth_type" name="auth_type">
            <n-space>
              <n-radio :value="0">前端菜单权限</n-radio>
              <n-radio :value="1">后端接口权限</n-radio>
            </n-space>
          </n-radio-group>
        </n-form-item>
        <n-form-item label="标题" path="label">
          <n-input placeholder="请输入标题" v-model:value="formParams.label" />
        </n-form-item>
        <n-form-item label="副标题" path="subtitle">
          <n-input placeholder="请输入副标题" v-model:value="formParams.subtitle" />
        </n-form-item>
        <n-form-item label="后端验证" path="is_check">
          <n-switch placeholder="请输入权限描述" v-model:value="formParams.is_check" />
        </n-form-item>
        <n-form-item label="权限名称" path="auth">
          <n-input placeholder="请输入权限名称" v-model:value="formParams.auth" />
        </n-form-item>
        <n-form-item label="权限描述" path="desc">
          <n-input placeholder="请输入权限描述" v-model:value="formParams.desc" />
        </n-form-item>
      </n-form>

      <template #footer>
        <n-space>
          <n-button type="primary" :loading="subLoading" @click="formSubmit">提交</n-button>
          <n-button @click="handleReset">重置</n-button>
        </n-space>
      </template>
    </n-drawer-content>
  </n-drawer>
</template>

<script lang="ts">
  import { defineComponent, reactive, ref, toRefs } from 'vue';
  import { useMessage } from 'naive-ui';
  import { addMenu } from '@/api/system/menu';

  const rules = {
    label: {
      required: true,
      message: '请输入标题',
      trigger: 'blur',
    },
    subtitle: {
      required: true,
      message: '请输入副标题',
      trigger: 'blur',
    },
    auth: {
      required: true,
      message: '请输入权限名称',
      trigger: 'blur',
    },
  };
  export default defineComponent({
    name: 'CreateDrawer',
    components: {},
    props: {
      title: {
        type: String,
        default: '添加顶级菜单',
      },
      width: {
        type: Number,
        default: 450,
      },
      pid: {
        type: Number,
        default: 0,
      },
      loadMenu: {
        type: Function,
        default: null,
      }
    },
    setup(props) {
      const message = useMessage();
      const formRef: any = ref(null);
      const defaultValueRef = () => ({
        id: 0,
        pid: 0,
        label: '',
        auth_type: 1,
        subtitle: '',
        is_check: false,
        auth: '',
        desc: '',
      });

      const state = reactive({
        isDrawer: false,
        subLoading: false,
        formParams: defaultValueRef(),
        placement: 'right' as const,
        alertText:
          '该功能主要实时预览各种布局效果，更多完整配置在 projectSetting.ts 中设置，建议在生产环境关闭该布局预览功能。',
      });

      function openDrawer() {
        state.isDrawer = true;
      }

      function closeDrawer() {
        state.isDrawer = false;
      }

      function formSubmit() {
        formRef.value.validate(async (errors) => {
          try {
            if (!errors) {
              state.formParams.pid = props.pid;
              const result = await addMenu(state.formParams);
              if(result) {
                message.success('添加成功');
                await props.loadMenu()
                handleReset();
                closeDrawer();
              }else {
                message.error('添加失败');
              }
            } else {
              message.error('请填写完整信息');
            }
          } catch (error) {}
        });
      }

      function handleReset() {
        formRef.value.restoreValidation();
        state.formParams = Object.assign(state.formParams, defaultValueRef());
      }

      return {
        ...toRefs(state),
        formRef,
        rules,
        formSubmit,
        handleReset,
        openDrawer,
        closeDrawer,
      };
    },
  });
</script>
