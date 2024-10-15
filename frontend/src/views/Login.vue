<template>
    <van-nav-bar title="登录" />
    <van-form @submit="onSubmit">
        <van-cell-group inset>
            <van-field v-model="username" name="用户名" label="用户名" placeholder="用户名"
                :rules="[{ required: true, message: '请填写用户名' }]" />
            <van-field v-model="password" type="password" name="密码" label="密码" placeholder="密码"
                :rules="[{ required: true, message: '请填写密码' }]" />
        </van-cell-group>
        <div style="margin: 16px;">
            <van-button round block type="primary" native-type="submit">
                登录
            </van-button>
        </div>
        <div style="margin: 16px;">
            <van-button round block type="default" @click="onRegisterClick">
                注册
            </van-button>
        </div>
    </van-form>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { ref, onMounted } from 'vue'
import api from '@/api'
import { showDialog, showNotify } from 'vant';
import { useUserStore } from '@/stores/user';
import encrypt from '@/utils/crypto';

const username = ref('')
const password = ref('')
const router = useRouter()
const userStore = useUserStore()
const onSubmit = () => {
    if (username.value !== '' && password.value !== '') {
        const param = {
            username: username.value,
            password: encrypt(password.value)
        }
        api.auth.login(param).then(res => {
            if (res.data.code === api.code.SUCCESS) {
                userStore.setToken(res.data.data)
                showNotify({ type: 'success', message: '登录成功' })
                router.push({ path: '/appointment' })
            } else {
                showNotify({ type: 'warning', message: res.data.msg })
            }
        })
    }
}

const onRegisterClick = () => {
    router.push({path: '/user/register'})
}

onMounted(() => {
    if (userStore.isLogin) {
        router.push({ path: "/user" });
    }
})
</script>

<style lang="scss" scoped></style>