<template>
    <van-nav-bar title="我的预约" left-text="返回" left-arrow @click-left="onClickLeft" />
</template>

<script setup>
const onClickLeft = () => history.back();
</script>

<style lang="scss" scoped>

</style>