<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router';
import { useUAStore } from '@/stores/ua.js';
import { onMounted } from 'vue';

const uaStore = useUAStore();

onMounted(() => {
  let ua = 0;
  if (/(iPhone|iPad|iPod|iOS)/i.test(navigator.userAgent)) {
    ua = 1;
  } else if (/(Android)/i.test(navigator.userAgent)) {
    ua = 2;
  } else {
    ua = 0;
  }
  uaStore.setUA({
    isMobile: ua === 1 || ua === 2,
    isPC: ua === 0,
  })
})
</script>

<template>
  <router-view></router-view>
</template>

<style scoped></style>
