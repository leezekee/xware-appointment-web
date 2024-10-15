import axios from 'axios'
import { showNotify } from 'vant';
import { useUserStore } from '@/stores/user';

const http = axios.create({
    baseURL: import.meta.env.VITE_BASE_URL,
    timeout: 5000,
});

http.interceptors.request.use(
    (config) => {
        const userStore = useUserStore();
        if (userStore.getToken) {
            config.headers.Authorization = userStore.getToken
        } else {
            config.headers.Authorization = ''
        }
        return config
    },
    (error) => {
        showNotify('请求失败，请稍后再试');
        return Promise.reject(error)
    }
)

// 请求拦截器
http.interceptors.response.use(
    (response) => {
        // if (response.status === 404) {
        //     // showFailToast('请先登录');
        //     return Promise.reject(response)
        // }
        let responseCode = response.data.code;
        // if (responseCode && responseCode != "200") {
        //         showFailToast('网络超时，请稍后再试');
        //     return response
        // }
        return response
    },
    (error) => {
        showNotify('请求失败，请稍后再试');
        return Promise.resolve(error.response)
    }
)

function post(url, params = {}) {
    return new Promise((resolve, reject) => {
        http({
            url,
            method: 'post',
            data: params,
            headers: {
                Accept: 'application/json',
                'Content-Type': 'application/json; charset=UTF-8'
            }
        }).then(res => {
            resolve(res)
        }).catch(err => {
            reject(err)
        })
    })
}

function get(url, params = {}) {
    return new Promise((resolve, reject) => {
        http({
            url,
            method: 'get',
            params,
            headers: {
                Accept: 'application/json',
                'Content-Type': 'application/json; charset=UTF-8'
            }
        }).then(res => {
            resolve(res)
        }).catch(err => {
            reject(err)
        })
    })
}

function del(url, params = {}) {
    return new Promise((resolve, reject) => {
        http({
            url,
            method: 'delete',
            params,
            headers: {
                Accept: 'application/json',
                'Content-Type': 'application/json; charset=UTF-8'
            }
        }).then(res => {
            resolve(res)
        }).catch(err => {
            reject(err)
        })
    })
}

function put(url, params = {}) {
    return new Promise((resolve, reject) => {
        http({
            url,
            method: 'put',
            data: params,
            headers: {
                Accept: 'application/json',
                'Content-Type': 'application/json; charset=UTF-8'
            }
        }).then(res => {
            resolve(res)
        }).catch(err => {
            reject(err)
        })
    })
}

function postMultipart(url, params = {}) {
    return new Promise((resolve, reject) => {
        http({
            url,
            method: 'post',
            data: params,
            headers: {
                Accept: 'application/json',
                'Content-Type': 'multipart/form-data; boundary=' + new Date().getTime()
            }
        }).then(res => {
            resolve(res)
        }).catch(err => {
            reject(err)
        })
    })
}

export {
    http,
    post,
    get,
    del,
    put,
    postMultipart
}