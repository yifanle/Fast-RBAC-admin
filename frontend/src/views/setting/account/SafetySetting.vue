<template>
  <n-grid cols="2 s:2 m:2 l:3 xl:3 2xl:3" responsive="screen">
    <n-grid-item>
      <n-form :label-width="80" :model="formValue" :rules="rules" ref="formRef">
        <n-form-item label="原密码" path="oldPassword">
          <n-input type="password" v-model:value="formValue.oldPassword" placeholder="请输入原密码" />
        </n-form-item>
        <n-form-item label="新密码" path="newPassword">
          <n-input type="password" v-model:value="formValue.newPassword" placeholder="请输入新密码" />
        </n-form-item>
        <n-form-item label="确认密码" path="reenterPassword">
          <n-input type="password" placeholder="请确认密码" v-model:value="formValue.reenterPassword" />
        </n-form-item>
        <div>
          <n-space>
            <n-button type="primary" @click="formSubmit">修改密码</n-button>
          </n-space>
        </div>
      </n-form>
    </n-grid-item>
  </n-grid>
</template>

<script lang="ts" setup>
  import { reactive, ref } from 'vue';
  import { useMessage } from 'naive-ui';
  import { FormItemRule } from 'naive-ui/lib/form/src/interface';
  import { updatePwd } from '@/api/system/user';
  import CryptoJS from "crypto-js";

  function validatePassword(rule: FormItemRule, value: string): boolean{
    return value === formValue.newPassword;
  }
  const rules = {
    newPassword: {
      required: true,
      message: '新密码不能为空',
      trigger: 'blur',
    },
    oldPassword: {
      required: true,
      message: '原密码不能为空',
      trigger: 'blur',
    },
    reenterPassword: [
      {
        required: true,
        message: '确认新密码不能为空',
        trigger: 'blur',
      },
      {
        validator: validatePassword,
        message: '两次密码输入不一致',
        trigger: 'blur'
      }
    ],
  };
  const formRef: any = ref(null);
  const message = useMessage();

  const formValue = reactive({
    newPassword: '',
    oldPassword: '',
    reenterPassword: '',
  });

  function formSubmit() {
    formRef.value.validate(async (errors) => {
      if (!errors) {
        try {
          formValue.oldPassword = CryptoJS.SHA256(formValue.oldPassword).toString(CryptoJS.enc.Hex);
          formValue.newPassword = CryptoJS.SHA256(formValue.newPassword).toString(CryptoJS.enc.Hex);
          formValue.reenterPassword = formValue.newPassword;
          const result = await updatePwd(formValue);
          if(result) {
            message.success('修改成功');
            Object.assign(formValue, {
              newPassword: '',
              oldPassword: '',
              reenterPassword: '',
            });
          }
        } catch (error) {
          Object.assign(formValue, {
              newPassword: '',
              oldPassword: '',
              reenterPassword: '',
            });
        }
      } else {
        message.error('验证失败，请填写完整信息');
      }
    });
  }
</script>
