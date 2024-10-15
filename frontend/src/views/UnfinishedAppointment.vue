<template>
    <van-nav-bar title="待维修" left-text="返回" left-arrow @click-left="onClickLeft" />
    <van-loading color="#1989fa" v-if="loading"/>
    <div class="card-list" v-else>
        <Card v-for="data in pendingList" :id="data.id" :time="data.time" :location="data.location"
            :appointmentStatus="data.appointmentStatus" :key="data.id" :problem-type="data.problemType"/>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import api from '@/api';

import Card from '@/components/Card.vue';
const onClickLeft = () => history.back();
const pendingList = ref([]);
const loading = ref(true);

onMounted(() => {
    api.appointment.getPendingAppointments().then((res) => {
        const list = res.data.data;
        console.log('getPendingAppointments', res.data.data);
        for (let i = 0; i < list.length; i++) {
            pendingList.value.push({
                id: list[i].id,
                time: list[i].start_time,
                location: "后勤楼F319",
                appointmentStatus: list[i].status,
                problemType: `${list[i].main_problem_type} - ${list[i].problem_type}`
            });
        }
    }).finally(() => {
        loading.value = false;
    })
})
</script>

<style lang="scss" scoped>
.card-list {
    height: 90vh;
    overflow-y: auto;
}
</style>