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
import { reactive, ref, onMounted } from 'vue'
import { showDialog } from 'vant';
import { useUserStore } from '@/stores/user';
import { useAppointmentStore } from '@/stores/appointment';
const appointmentStore = useAppointmentStore();
const userStore = useUserStore();
const appointmentInfo = reactive({
    timeSolt: '',
    faultType: '',
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
    appointmentInfo.timeSolt = selectedOptions;
    timeSolt.value = selectedOptions[0].text + " " + selectedOptions[1].text;
};
const faultTypeOnConfirm = ({ selectedOptions }) => {
    showFaultTypePicker.value = false;
    appointmentInfo.faultType = selectedOptions;
    faultType.value = selectedOptions[0].text + " " + selectedOptions[1].text;
};
const getTimeSlotData = () => {
    showTimeSlotPicker.value = true;
    timeSoltLoading.value = true;
    timeSoltColumns.value = [
        {
            text: '2023-10-20',
            value: '2023-10-20',
            children: [
                { text: '下午18:00-20:00', value: 1 },
                { text: '下午20:00-22:00', value: 2 },
            ],
        },
        {
            text: '2023-10-27',
            value: '2023-10-27',
            children: [
                { text: '下午18:00-20:00', value: 1 },
                { text: '下午20:00-22:00', value: 2 },
            ],
        },
    ];
    timeSoltLoading.value = false;
}
const getFaultTypeData = () => {
    showFaultTypePicker.value = true;
    faultTypeLoading.value = true;
    faultTypeColumns.value = [
        {
            text: '软件问题',
            value: '软件问题',
            children: [
                { text: '无法访问互联网', value: '无法访问互联网' },
                { text: '无法访问互联网', value: '无法访问互联网' }
            ],
        },
        {
            text: '硬件问题',
            value: '硬件问题',
            children: [
                { text: '清灰', value: '清灰' },
                { text: '清灰', value: '清灰' }
            ],
        }
    ];
    faultTypeLoading.value = false;
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
        showDialog({
            message: '您还没有登录，请先登录',
        }).then(() => {
            router.push('/user/login');
        });
        return;
    }
    if (!comfirmDetail()) {
        return;
    }
    submitAppointment();
};
const comfirmDetail = () => {
    if (appointmentInfo.detail === '') {
        showNoDetailComfirm.value = true;
        return false;
    }
}
const uploadAppointment = () => {
    console.log(appointmentInfo);
    // TODO 提交预约信息


    return true;
}
const submitAppointment = () => {
    if (uploadAppointment()) {
        showDialog({
            message: '预约成功！请您在预约时间段内到后勤楼F319进行维修，如有特殊情况，我们会在企业微信中联系您',
        }).then(() => {
            timeSolt.value = '';
            faultType.value = '';
            appointmentInfo.detail = '';
            appointmentInfo.timeSolt = '';
            appointmentInfo.faultType = '';
        });
    } else {
        showDialog({
            message: '预约失败，请稍后重试或在公众号中联系我们',
        }).then(() => { });
    }
}

onMounted(() => {
    if (userStore.hasLogin && appointmentStore.hasCache) {
        appointmentInfo.value = appointmentStore.getAppointmentInfo();
        appointmentStore.clearCache();
    }
})
</script>

<style lang="scss" scoped></style>