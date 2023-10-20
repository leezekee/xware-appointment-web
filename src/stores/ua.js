import { ref } from 'vue'
import { defineStore } from 'pinia'

export const useUAStore = defineStore('ua', () => {
    const ua = ref({
        isMobile: true,
        isPC: false
    });
    const setUA = (_ua) => {
        ua.value = _ua;
    }

    return { ua, setUA }
})