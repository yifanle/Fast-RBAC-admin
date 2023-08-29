<template>
  <n-grid cols="2 s:2 m:2 l:3 xl:3 2xl:3" responsive="screen">
    <n-grid-item>
      <n-form :label-width="80"
            class="py-8" :model="formValue" :rules="rules" ref="formRef">
        <n-form-item label="昵称" path="nickname">
          <n-input v-model:value="formValue.nickname" placeholder="请输入昵称" />
        </n-form-item>
        <n-form-item label="姓名" path="realName">
          <n-input v-model:value="formValue.realName" placeholder="请输入姓名" />
        </n-form-item>
        <n-form-item label="邮箱" path="user_email">
          <n-input placeholder="请输入邮箱" v-model:value="formValue.user_email" />
        </n-form-item>

        <n-form-item label="联系电话" path="user_phone">
          <n-input placeholder="请输入联系电话" v-model:value="formValue.user_phone" />
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
        <n-form-item label="描述信息" path="desc">
          <n-input v-model:value="formValue.desc" type="textarea" placeholder="请输入描述信息" />
        </n-form-item>

        <div>
          <n-space>
            <n-button type="primary" @click="formSubmit">更新基本信息</n-button>
          </n-space>
        </div>
      </n-form>
    </n-grid-item>
  </n-grid>
</template>

<script lang="ts" setup>
  import { reactive, ref } from 'vue';
  import { useMessage } from 'naive-ui';
  import { UserInfoType, useUserStore } from '@/store/modules/user';
  import { FormItemRule } from 'naive-ui/lib/form/src/interface';
  import { updateAccount } from '@/api/system/user';

  const useUser = useUserStore();
  const userInfo: UserInfoType = useUser.getUserInfo;
  function validateUsername(rule: FormItemRule, value: string): boolean{
    if(value.length>3&&value.length<20){
      return true;
    }else{
      return false;
    }
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
    realName: [
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
  const formRef: any = ref(null);
  const message = useMessage();

  const formValue = reactive({...userInfo});

  function formSubmit() {
    formRef.value.validate(async (errors) => {
      if (!errors) {
        try {
          const result = await updateAccount(formValue)
          if(result) {
            message.success('修改成功');
            const info = useUser.getInfo();
            Object.assign(formValue, info);
          }
        } catch (error) {}
      } else {
        message.error('验证失败，请填写完整信息');
      }
    });
  }
</script>
