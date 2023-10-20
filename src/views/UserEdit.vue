<template>
    <van-nav-bar title="标题" left-text="返回" left-arrow @click-left="onClickLeft" />
    <van-form @submit="onSubmit">
        <van-cell-group inset>
            <van-field v-model="username" name="用户名" label="用户名" placeholder="用户名"
                :rules="[{ required: true, message: '请填写用户名', validator: usernameValidator }]" />
            <van-field v-model="sid" name="学号" label="学号" placeholder="请输入正确的学号以便我们联系您"
                :rules="[{ required: true, message: '请填写学号', validator: sidValidator }]" />
            <van-field v-model="tel" name="联系方式" label="联系方式" placeholder="联系方式"
                :rules="[{ required: true, message: '请填写联系方式', validator: telValidator }]" />
        </van-cell-group>
        <div style="margin: 16px;">
            <van-button round block type="primary" native-type="submit">
                提交
            </van-button>
        </div>
    </van-form>
</template>

<script setup>
import { ref } from 'vue';
import { useUserStore } from '@/stores/user';
import api from '@/api';
import { showSuccessToast } from 'vant';
import router from '@/router';

const username = ref('');
const sid = ref('');
const tel = ref('');
const userStore = useUserStore();

const usernameValidator = (value, rule) => {
    if (value.length < 2) {
        return '用户名长度不能小于2';
    }
    if (value.length > 10) {
        return '用户名长度不能大于10';
    }
    if (/^\d+$/.test(value)) {
        return '用户名不能为纯数字';
    }
    return true;
}
const sidValidator = (value, rule) => {
    if (!/^\d{10}$/.test(value)) {
        return '请输入正确的学号';
    }
    return true;
}
const telValidator = (value, rule) => {
    if (!/^\d{11}$/.test(value)) {
        return '请输入正确的手机号码';
    }
    return true;
}
const onClickLeft = () => history.back();
const onSubmit = () => {
    // api.auth.updateUserInfo({
    //     username: username.value,
    //     sid: sid.value,
    //     tel: tel.value,
    // }).then((res) => {
        userStore.changeInfo(username.value, sid.value, tel.value);
        showSuccessToast('修改成功！');
        router.go(-1);
    // }).catch((res) => {
        
        // })
}
</script>

<style lang="scss" scoped></style>