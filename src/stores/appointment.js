import { computed, reactive } from 'vue';
import { defineStore } from 'pinia';

export const useAppointmentStore = defineStore('appointment', () => {
    const appointmentInfo = reactive({
        timeSolt: '',
        faultType: '',
        detail: ''
    })

    const setAppointmentInfo = (_appointmentInfo) => { 
        appointmentInfo.timeSolt = _appointmentInfo?.timeSolt
        appointmentInfo.faultType = _appointmentInfo?.faultType
        appointmentInfo.detail = _appointmentInfo?.detail
    }
    const getAppointmentInfo = computed(() => appointmentInfo)
    const clearCache = () => { 
        appointmentInfo.timeSolt = ''
        appointmentInfo.faultType = ''
        appointmentInfo.detail = ''
    }
    const hasCache = computed(() => appointmentInfo.timeSolt !== '' || appointmentInfo.faultType !== '' || appointmentInfo.detail !== '')

    return {
        appointmentInfo,
        setAppointmentInfo,
        clearCache,
        getAppointmentInfo,
        hasCache
    }
})