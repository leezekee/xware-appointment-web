<template>
    <van-nav-bar title="编辑" left-text="返回" left-arrow @click-left="onClickLeft" />
    <van-loading color="#1989fa" v-if="loading"/>
    <van-form @submit="onSubmit" v-else>
        <van-cell-group inset>
            <van-field v-model="sid" name="学号" label="学号" placeholder="请正确填写以便我们联系您"
                :rules="[{ validator: sidValidator }]" />
            <van-field v-model="tel" name="联系方式" label="联系方式" placeholder="请正确填写以便我们联系您"
                :rules="[{ validator: telValidator }]" />
            <van-field v-model="email" name="邮箱" label="邮箱" placeholder="请正确填写以便我们联系您"
                :rules="[{ validator: emailValidator }]" /> </van-cell-group>
        <div style="margin: 16px;">
            <van-button round block type="primary" native-type="submit">
                提交
            </van-button>
        </div>
    </van-form>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useUserStore } from '@/stores/user';
import api from '@/api';
import { showSuccessToast, showNotify } from 'vant';
import router from '@/router';

const email = ref('');
const sid = ref('');
const tel = ref('');
const oldInfo = ref({});
const userStore = useUserStore();
const loading = ref(false);

const emailValidator = (value, rule) => {
    if (!/^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$/.test(value)) {
        return '请输入正确的邮箱';
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
    let params = {}
    if (email.value !== oldInfo.email) {
        params.email = email.value;
    } else {}
    if (sid.value !== oldInfo.sid) {
        params.sid = sid.value;
    }
    if (tel.value !== oldInfo.tel) {
        params.phone = tel.value;
    }
    if (Object.keys(params).length === 0) {
        showNotify({ type: 'warning', message: '未修改任何信息' });
        return;
    }
    api.auth.updateUserInfo(params).then((res) => {
        if (res.data.code == api.code.SUCCESS) {
            userStore.changeInfo(params);
            router.push({ path: '/user' });
            showNotify({ type: 'success', message: '修改成功' });
        } else {
            showNotify({ type: 'warning', message: res.data.msg });
        }
    })
}

onMounted(() => {
    loading.value = false;
    api.auth.getUserInfo().then((res) => {
        // console.log('getUserInfo', res.data.data);
        email.value = res.data.data.email;
        sid.value = res.data.data.sid;
        tel.value = res.data.data.phone;
        oldInfo.email = res.data.data.email;
        oldInfo.sid = res.data.data.sid;
        oldInfo.tel = res.data.data.phone;
        
    }).finally(() => {
        loading.value = false;
    })
})
</script>

<style lang="scss" scoped></style>