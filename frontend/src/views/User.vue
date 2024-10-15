<template>
    <router-view></router-view>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user';
const userStore = useUserStore();

import { onMounted } from 'vue'
const router = useRouter()
onMounted(() => {
    if (!userStore.isLogin) {
        router.push({path: '/user/login'})
    }
})
</script>

<style lang="scss" scoped>

</style>