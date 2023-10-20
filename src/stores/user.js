import { ref, computed } from 'vue';
import { defineStore } from 'pinia';

export const useUserStore = defineStore('user', () => {
    const username = ref('冬素廿六');
    const sid = ref('');
    const tel = ref('');
    const avatar = computed(() => username.value !== '' ? username.value[0] : '')

    const setUsername = (_username) => {
        username.value = _username;
    }
    const setSid = (_sid) => {
        sid.value = _sid;
    }
    const setTel = (_tel) => {
        tel.value = _tel;
    }
    const hasLogin = computed(() => username.value !== '');
    const changeInfo = (_username, _sid, _tel) => {
        setUsername(_username);
        setSid(_sid);
        setTel(_tel);
    }

    return {
        username,
        sid,
        tel,
        avatar,
        setUsername,
        setSid,
        setTel,
        hasLogin,
        changeInfo
    }
})