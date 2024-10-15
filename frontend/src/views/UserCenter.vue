<template>
    <van-loading color="#1989fa" v-if="loading"/>
    <div class="user-container" v-else>
        <div class="header">
            <div class="avatar">
                {{ avatar }}
            </div>
            <div class="username">
                {{ username }}
            </div>
            <div class="flex-growth"></div>
            <router-link class="edit" to="/user/edit">编辑</router-link>
            <span class="logout" @click="logout">登出</span>
        </div>
        <van-grid clickable :column-num="2">
            <van-grid-item icon="notes-o" v-if="todoSum != 0" :badge="todoSum" text="待维修" to="/user/mine" />
            <van-grid-item icon="notes-o" v-else text="待维修" to="/user/mine" />
            <van-grid-item icon="todo-list-o" text="全部预约" to="/user/history" />
        </van-grid>
    </div>
</template>

<script setup>
import { ref, toRef, onMounted } from 'vue';
import { useUserStore } from '@/stores/user';
import api from '@/api';
import router from '@/router';
import { showNotify } from 'vant';

const userStore = useUserStore();
const todoSum = ref(0);
const username = toRef(userStore, 'username');
const avatar = toRef(userStore, 'avatar');
const loading = ref(true);

const logout = () => {
    api.auth.logout().then((res) => {
        if (res.data.code == api.code.SUCCESS) {
            userStore.logout();
            showNotify({ type: 'success', message: '登出成功' });
            router.push({ path: '/user/login' });
        } else {
            showNotify({ type: 'warning', message: '登出失败' });
        }
    })
}

onMounted(() => {
    api.auth.getUserInfo().then((res) => {
        // console.log('getUserInfo', res.data.data);
        userStore.changeInfo(res.data.data);
        todoSum.value = res.data.data.pending_count
    }).finally(() => {
        loading.value = false;
    })
})
</script>

<style lang="scss" scoped>
.user-container {
    display: flex;
    flex-direction: column;

    .header {
        display: flex;
        align-items: center;
        height: 150px;

        .avatar {
            display: flex;
            justify-content: center;
            align-self: center;
            width: 100px;
            height: 100px;
            line-height: 100px;
            border-radius: 50%;
            background-color: #ecf5ff;
            margin-left: 30px;
            font-size: 50px;
            font-weight: 400;
            color: #606266;
            user-select: none;
        }

        .username {
            font-size: 24px;
            font-weight: 400;
            color: #606266;
            margin-left: 20px;
        }
        .edit {
            font-size: 16px;
            font-weight: 400;
            color: #6397ff;
            margin-right: 30px;
            cursor: pointer;
        }
        .logout {
            font-size: 16px;
            font-weight: 400;
            color: #da3030;
            margin-right: 30px;
            cursor: pointer;
        }
    }
}
</style>