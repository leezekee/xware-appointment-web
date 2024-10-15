<template>
    <div class="card-wrapper" :class="cardClass" @click="onCardClick(id)">
        <div class="card-content">
            <div class="left-info">
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
                    <span>问题类型: </span>
                    <span>{{ problemType }}</span>
                </div>
                <div class="line">
                    <span>预约状态: </span>
                    <span>{{ appointmentStatus }}</span>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue';
import Document from '@/components/icon/Document.vue';
import Success from '@/components/icon/Success.vue'
import Cancel from '@/components/icon/Cancel.vue'
import Overdue from '@/components/icon/Overdue.vue'
import { computed } from 'vue';
import router from '@/router';

const props = defineProps(['id', 'time', 'location', 'appointmentStatus',  'problemType']);
const emit = defineEmits(['card:click'])

const id = computed(() => props.id)
const time = computed(() => props.time)
const location = computed(() => props.location)
// const location = "后勤楼F319"
const appointmentStatus = computed(() => props.appointmentStatus)
const problemType = computed(() => props.problemType)

const cardClass = computed(() => {
    if (appointmentStatus.value === '待维修') {
        return 'unfinished'
    } else if (appointmentStatus.value === '已完成') {
        return 'finished'
    } else if (appointmentStatus.value == "已过期") {
        return 'overdue'
    } else {
        return 'cancel'
    }
})

const onCardClick = (id) => {
    router.push({
        path: '/user/appointmentDetail',
        query: {
            id
        }
    })
}
</script>

<style lang="scss" scoped>
.card-wrapper {
    display: flex;
    padding-left: 30px;
    align-items: center;
    border-radius: 10px;
    height: 120px;
    width: 90%;
    margin: auto;
    margin-top: 10px;
    overflow: hidden;
    cursor: pointer;

    .card-content {
        display: flex;
        align-items: center;
        width: 100%;
        .left-info {
            display: flex;
            flex-direction: column;
            flex: 10;
            .line {
                display: flex;

                // width: 200px;
                // text-overflow: ellipsis;

                span:nth-child(1) {
                    font-weight: bold;
                    margin-right: 10px;
                }
                span:nth-child(2) {
                    width: 70%;
                    overflow: hidden;
                    text-overflow: ellipsis;
                    white-space: nowrap;
                }
            }
        }
    }
}

.card-wrapper::ber {
    background: url('@/assets/Success.svg') no-repeat right center;
}

.finished {
    border: 1px solid #096530;
    color: #096530;
    background: url('@/assets/Success.svg') no-repeat right center;

}

.unfinished {
    border: 1px solid black;
    color: black;
    background: url('@/assets/Document.svg') no-repeat right center;
}

.cancel {
    border: 1px solid #9f291a;
    color: #9f291a;
    background: url('@/assets/Cancel.svg') no-repeat right center;
}

.overdue {
    border: 1px solid rgb(190, 190, 190);
    color: #606266;
    background: url('@/assets/Overdue.svg') no-repeat right center;
}

.card-wrapper:hover {
    background-color: #f0f0f0;
}
</style>