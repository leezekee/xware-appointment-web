<template>
    <van-nav-bar title="注册" />
    <van-form @submit="onSubmit">
        <van-cell-group inset>
            <van-field v-model="username" name="用户名" label="用户名" placeholder="用户名"
                :rules="[{ required: true, message: '请填写用户名' }]" />
            <van-field v-model="password" type="password" name="密码" label="密码" placeholder="密码"
                :rules="[{ required: true, message: '请填写密码' }]" />
            <van-field v-model="repassword" type="password" name="确认密码" label="确认密码" placeholder="确认密码"
                :rules="[{ validator: checkRepassword }]" />
            <van-field v-model="sid" name="学号" label="学号" placeholder="请填写学号（请正确填写确保我们可以联系到）"
                :rules="[{ validator: checkSid }]" />
            <van-field v-model="phone" name="电话" label="电话" placeholder="请填写电话（请正确填写确保我们可以联系到）"
                :rules="[{ validator: checkPhone }]" />
            <van-field v-model="email" name="邮箱" label="邮箱" placeholder="请填写邮箱（请正确填写确保我们可以联系到）"
                :rules="[{ validator: checkEmail }]" />
        </van-cell-group>
        <div style="margin: 16px;">
            <van-button round block type="primary" native-type="submit">
                注册
            </van-button>
        </div>
        <div style="margin: 16px;">
            <van-button round block type="default" @click="onLoginClick">
                登录
            </van-button>
        </div>
    </van-form>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { ref, onMounted } from 'vue'
import api from '@/api'
import User from './User.vue';
import { showDialog, showNotify } from 'vant';
import { useUserStore } from '@/stores/user';
import encrypt from '@/utils/crypto';

const username = ref('')
const password = ref('')
const repassword = ref('')
const sid = ref('')
const phone = ref('')
const email = ref('')
const router = useRouter()
const userStore = useUserStore()
const onSubmit = () => {
    const enpassword = encrypt(password.value)
    const enrepassword = encrypt(repassword.value)
    const param = {
        username: username.value, 
        password: enpassword,
        repassword: enrepassword,
        sid: sid.value,
        phone: phone.value,
        email: email.value
    }
    // console.log('param', param);
    api.auth.register(param).then(res => {
        if (res.data.code == api.code.SUCCESS) {
            const data = res.data.data
            userStore.setToken(data.data)
            showNotify({ type: 'success', message: '注册成功' })
            router.push({ path: '/appointment' })
        } else {
            showNotify({ type: 'warning', message: res.data.msg })
        }
    })
}

const checkRepassword = () => {
    if (password.value != repassword.value) {
        return "两次密码不一致"
    } else if (repassword.value == '') {
        return "请确认密码"
    }
}

const onLoginClick = () => {
    router.push({ path: '/user/login' })
}

const checkSid = () => {
    if (sid.value == '') {
        return "请填写学号"
    }
    const reg = /^[0-9]{10}$/
    if (!reg.test(sid.value)) {
        return "学号格式错误"
    }
}

const checkPhone = () => {
    if (phone.value == '') {
        return "请填写电话"
    }
    const reg = /^[0-9]{11}$/
    if (!reg.test(phone.value)) {
        return "电话格式错误"
    }
}

const checkEmail = () => {
    if (email.value == '') {
        return "请填写邮箱"
    }
    const reg = /^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$/
    if (!reg.test(email.value)) {
        return "邮箱格式错误"
    }
}

onMounted(() => {
    if (userStore.isLogin) {
        router.push({ path: "/user" });
    }
})
</script>

<style lang="scss" scoped></style>