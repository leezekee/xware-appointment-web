<template>
    <van-loading color="#1989fa" v-if="loading" />
    <div v-else>
        <van-nav-bar title="预约详情" left-text="返回" left-arrow @click-left="onClickLeft" />
        <div class="content">
            <div class="line">
                <span>预约编号: </span>
                <span>{{ id }}</span>
            </div>
            <div class="line">
                <span>预约时间: </span>
                <span>{{ time }}</span>
            </div>
            <div class="line">
                <span>预约地点: </span>
                <span>{{ location }}</span>
            </div>
            <div class="line">
                <span>预约状态: </span>
                <span>{{ appointmentStatus }}</span>
            </div>
            <div class="line">
                <span>问题类型: </span>
                <span>{{ problem }}</span>
            </div>
            <div class="line">
                <span>问题描述: </span>
                <span>{{ description }}</span>
            </div>
            <van-button plain type="danger" class="btn" @click="cancelConfirm" v-if="isPending">取消预约</van-button>
            <!-- <van-button plain type="primary" class="btn" @click="cancelConfirm"
                v-else-if="isCanceled||isOverDue">重新预约</van-button> -->
            <span class="finish" v-else-if="isCanceled || isOverDue">工单已取消，如有需求，请重新预约</span>
            <span class="finish" v-else-if="isCompleted">工单已完成，如有疑问请联系我们</span>
        </div>
    </div>
</template>

<script setup>
import api from '@/api';
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { showConfirmDialog, showNotify } from 'vant';
import { computed } from 'vue';

const onClickLeft = () => history.back();
const id = ref(-1);
const loading = ref(true);
const time = ref('');
const location = ref('');
const appointmentStatus = ref('');
const problem = ref('');
const description = ref('');
const router = useRouter();

const route = useRoute();

const cancelConfirm = () => {
    showConfirmDialog({
        title: '提示',
        message: '确定取消预约？',
    }).then(() => {
        console.log('cancel', id.value);
        api.appointment.cancelAppointment(id.value).then((res) => {
            console.log('cancelAppointment', res);
            if (res.data.code == api.code.SUCCESS) {
                showNotify({ type: 'success', message: res.data.msg });
            } else {
                showNotify({ type: 'warning', message: res.data.msg });
            }
        }).finally(() => {
            router.go(0)
        })
    });
}

const reAppointment = () => {
    showConfirmDialog({
        title: '提示',
        message: '确定重新预约？',
    }).then(() => {
        api.appointment.createAppointment(parma).then((res) => {
            console.log('reAppointment', res);
            if (res.data.code == api.code.SUCCESS) {
                showNotify({ type: 'success', message: res.data.msg });
            } else {
                showNotify({ type: 'warning', message: res.data.msg });
            }
        }).finally(() => {
            router.go(0)
        })
    });
}

const isCanceled = computed(() => { 
    return appointmentStatus.value === '已取消';
})

const isOverDue = computed(() => { 
    return appointmentStatus.value === '已过期';
})

const isPending = computed(() => { 
    return appointmentStatus.value === '待维修';
})

const isCompleted = computed(() => { 
    return appointmentStatus.value === '已完成';
})

onMounted(() => {
    id.value = route.query.id;
    api.appointment.getAppointmentDetail(id.value).then((res) => {
        const data = res.data.data;
        console.log('getAppointmentDetail', data);
        time.value = data.start_time;
        location.value = "后勤楼F319";
        appointmentStatus.value = data.status;
        problem.value = `${data.main_problem_type} - ${data.problem_type}`;
        description.value = data.description || '无'
    }).finally(() => {
        loading.value = false;
    })
})
</script>

<style lang="scss" scoped>
.content {
    padding: 16px;
    .line {
        display: flex;
        justify-content: space-between;
        margin-bottom: 16px;
        span {
            font-size: 16px;
            color: #333;
        }

        span:last-child {
            max-width: 70%;
        }
    }

    .btn {
        margin-top: 20px;
        width: 100%;
    }

    .finish {
        color: #999;
        font-size: 14px;
    }
}
</style>