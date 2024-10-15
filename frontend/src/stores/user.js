import { ref, computed } from 'vue';
import { defineStore } from 'pinia';
import { jwtDecode } from "jwt-decode";

export const useUserStore = defineStore('user', () => {
    const username = ref('');
    const sid = ref('');
    const tel = ref('');
    const email = ref('');
    const token = ref('');
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
    const setEmail = (_email) => {
        email.value = _email;
    }
    const isLogin = computed(() => token.value !== '');
    // 时间太久忘了这个是干什么的了，先留着
    const hasLogin = computed(() => token.value !== '');
    const changeInfo = (info) => {
        const {sid:_sid, phone:_tel, email:_email} = info;
        setSid(_sid);
        setTel(_tel);
        setEmail(_email);
    }
    const getInfo = computed(() => { 
        return {
            username: username.value,
            sid: sid.value,
            tel: tel.value,
            email: email.value
        }
    })
    const getToken = computed(() => token.value)    
    const setToken = (_token) => {
        token.value = _token;
        try {
            const decoded = jwtDecode(_token);
            username.value = decoded.username;
        }
        catch (e) {
            console.log("token解析失败");
            username.value = '';
        }
    }

    const getUsername = computed(() => username.value);

    const logout = () => { 
        token.value = '';
        username.value = '';
        sid.value = '';
        tel.value = '';
        email.value = '';
    }

    return {
        avatar,
        hasLogin,
        changeInfo,
        isLogin,
        getInfo,
        token,
        username,
        setUsername,
        getUsername,
        getToken,
        setToken,
        logout
    }
}, {
    persist: {
        enabled: true,
        strategies: [
            {
                key: 'dXNlcg',
                storage: localStorage,
                paths: ['token', 'username'],
            },
        ],
    }
})