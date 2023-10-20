import axios from 'axios'
import { showFailToast } from 'vant';

const http = axios.create({
    baseURL: 'http://localhost:8080',
    timeout: 5000,
    headers: {
        'token': localStorage.getItem('token') || ''
    },
});

// 请求拦截器
http.interceptors.response.use(
    (response) => {
        let responseCode = response.data.code;
        if (responseCode && responseCode != "200") {
                showFailToast('网络超时，请稍后再试');
            return response
        }
        return response
    },
    (error) => {
        if (error.code === 'ECONNABORTED' || error.message === "Network Error" || error.message.includes("timeout")) {
                showFailToast('网络超时，请稍后再试');
        }
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