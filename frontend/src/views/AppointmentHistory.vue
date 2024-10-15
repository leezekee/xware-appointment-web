<template>
    <van-nav-bar title="我的预约" left-text="返回" left-arrow @click-left="onClickLeft" />
    <van-loading color="#1989fa" v-if="loading"/>
    <div class="card-list" v-else>
        <Card v-for="data in allList" :id="data.id" :time="data.time" :location="data.location"
            :appointmentStatus="data.appointmentStatus" :key="data.id" :problem-type="data.problemType"/>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import api from '@/api';
const onClickLeft = () => history.back();
const allList = ref([]);
const loading = ref(true);

onMounted(() => {
    api.appointment.getAppointmentList().then((res) => {
        const list = res.data.data;
        console.log('getAppointmentList', res.data.data);
        for (let i = 0; i < list.length; i++) {
            allList.value.push({
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