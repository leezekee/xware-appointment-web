<template>
    <van-nav-bar title="X-Ware 服务预约" />
    <van-form @submit="onSubmit">
        <van-cell-group>
            <van-field v-model="timeSolt" is-link readonly label="时间段" placeholder="选择时间段" @click="getTimeSlotData" 
                :rules="[{ required: true, message: '请选择时间段' }]" />
            <van-popup v-model:show="showTimeSlotPicker" round position="bottom">
                <van-picker :columns="timeSoltColumns" @cancel="showTimeSlotPicker = false" @confirm="timeSoltOnConfirm"
                    :loading="timeSoltLoading" />
            </van-popup>
        </van-cell-group>
        <van-cell-group>
            <van-field v-model="faultType" is-link readonly label="故障类型" placeholder="选择故障类型" @click="getFaultTypeData" 
                :rules="[{ required: true, message: '请选择故障类型' }]" />
            <van-popup v-model:show="showFaultTypePicker" round position="bottom">
                <van-picker :columns="faultTypeColumns" @cancel="showPicker = false" @confirm="faultTypeOnConfirm"
                    :loading="faultTypeLoading" />
            </van-popup>
        </van-cell-group>
        <van-cell-group>
            <van-field v-model="appointmentInfo.detail" rows="5" autosize label="故障详情描述" type="textarea" maxlength="200"
                placeholder="请输入故障详情与描述" show-word-limit />
        </van-cell-group>
        <div style="margin: 16px;">
            <van-button round block type="primary" native-type="submit">
                提交
            </van-button>
        </div>
    </van-form>
    <van-dialog 
        v-model:show="showNoDetailComfirm" 
        title="提示" 
        show-cancel-button 
        @confirm="noDetailOnConfirm" 
        @cancel="noDetailOnCancel">
        <div class="van-dialog__message">
            您没有填写故障详情描述，填写故障详情描述可以帮助我们更好的做好维修准备，是否继续提交？
        </div>
    </van-dialog>
</template>

<script setup>
import { reactive, ref, onMounted, onUnmounted } from 'vue'
import { showDialog } from 'vant';
import { useUserStore } from '@/stores/user';
import { useAppointmentStore } from '@/stores/appointment';
import { showNotify, closeNotify } from 'vant';
import router from '@/router';
import api from '@/api';

const appointmentStore = useAppointmentStore();
const userStore = useUserStore();
const appointmentInfo = reactive({
    timeSolt: '',
    problemType: '',
    detail: ''
})
const timeSoltLoading = ref(true);
const faultTypeLoading = ref(true);
const timeSolt = ref('');
const faultType = ref('');
const showTimeSlotPicker = ref(false);
const showFaultTypePicker = ref(false);
const showNoDetailComfirm = ref(false);
const timeSoltColumns = ref([]);
const faultTypeColumns = ref([]);

const timeSoltOnConfirm = ({ selectedOptions }) => {
    showTimeSlotPicker.value = false;
    appointmentInfo.timeSolt = selectedOptions[0].value;
    timeSolt.value = selectedOptions[0].text;
};
const faultTypeOnConfirm = ({ selectedOptions }) => {
    console.log('faultTypeOnConfirm', selectedOptions[1].value);
    showFaultTypePicker.value = false;
    appointmentInfo.problemType = selectedOptions[1].value;
    faultType.value = selectedOptions[0].text + " - " + selectedOptions[1].text;
};
const getTimeSlotData = () => {
    timeSoltColumns.value = [];
    showTimeSlotPicker.value = true;
    timeSoltLoading.value = true;
    api.appointment.getTimeSlot().then((res) => {
        console.log('getTimeSlot', res.data.data);
        for (let i = 0; i < res.data.data.length; i++) {
            let row = {}
            row.text = res.data.data[i].start + ' - ' + res.data.data[i].end;
            row.value = res.data.data[i].id;
            timeSoltColumns.value.push(row);
        }
    }).finally(() => {
        timeSoltLoading.value = false;
    })
    timeSoltLoading.value = false;
}
const getFaultTypeData = () => {
    faultTypeColumns.value = [];
    showFaultTypePicker.value = true;
    faultTypeLoading.value = true;
    api.appointment.getProblemType().then((res) => {
        // 遍历keyvalue
        for (let key in res.data.data) {
            let row = {}
            row.text = key;
            row.value = key;
            row.children = [];
            for (let i = 0; i < res.data.data[key].length; i++) {
                let child = {};
                child.text = res.data.data[key][i].type;
                child.value = res.data.data[key][i].id;
                row.children.push(child);
            }
            faultTypeColumns.value.push(row);
        }
        console.log('getFaultType', faultTypeColumns.value);
    }).finally(() => {
        faultTypeLoading.value = false;
    })
}
const noDetailOnConfirm = () => {
    showNoDetailComfirm.value = false;
    submitAppointment();
}
const noDetailOnCancel = () => {
    showNoDetailComfirm.value = false;
}
const onSubmit = () => {
    if (!userStore.hasLogin) {
        showNotify({ type: 'primary', message: '暂未登录，请先登录' });
        router.push({ path: '/user/login' });
        return;
    }
    comfirmDetail();
};
const comfirmDetail = () => {
    if (appointmentInfo.detail === '') {
        showNoDetailComfirm.value = true;
    } else {
        submitAppointment();
    }
}

const submitAppointment = () => {
    const params = {
        timeslot_id: appointmentInfo.timeSolt,
        problem_id: appointmentInfo.problemType,
        description: appointmentInfo.detail
    }
    console.log('submit', params);
    api.appointment.createAppointment(params).then((res) => {
        if (res.data.code == api.code.SUCCESS) {
            showDialog({
                message: '预约成功！请您在预约时间段内到后勤楼F319进行维修，如有特殊情况，我们会在企业微信中联系您',
            }).then(() => {
                timeSolt.value = '';
                faultType.value = '';
                appointmentInfo.detail = '';
                appointmentInfo.timeSolt = '';
                appointmentInfo.problemType = '';
            });
        } else {
            showDialog({
                message: `预约失败，请稍后重试或在公众号中联系我们
                错误信息：${res.data.message}`,
            }).then(() => { });
        }
    })
}

onMounted(() => {
    if (userStore.hasLogin && appointmentStore.hasCache) {
        appointmentInfo.value = appointmentStore.getAppointmentInfo();
        appointmentStore.clearCache();
    }
    if (!userStore.isLogin) {
        showNotify({ type: 'primary', message: '暂未登录，请先登录' });
    }
})

onUnmounted(() => {
    closeNotify()
})
</script>

<style lang="scss" scoped></style>