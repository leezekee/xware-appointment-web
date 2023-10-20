<template>
    <van-nav-bar title="待维修" left-text="返回" left-arrow @click-left="onClickLeft" />
</template>

<script setup>
const onClickLeft = () => history.back();
</script>

<style lang="scss" scoped></style>