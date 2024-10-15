<template>
    <router-view></router-view>
    <van-tabbar v-model="active">
        <van-tabbar-item name="home" icon="home-o" to="/appointment">预约</van-tabbar-item>
        <van-tabbar-item name="user" icon="manager" to="/user">我的</van-tabbar-item>
    </van-tabbar>
</template>

<script setup>
import { ref } from 'vue'
const active = ref(window.location.pathname.includes('/appointment') ? 'home' : 'user');
</script>

<style lang="scss" scoped></style>