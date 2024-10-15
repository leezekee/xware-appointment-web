import {
    http,
    get,
    post,
    del,
    put
} from './axios';

let userApi = {
    login: (params) => post('/login', params),
    register: (params) => post('/register', params),
    logout: () => post('/logout'),
    getUserInfo: () => get('/user/info'),
    updateUserInfo: (params) => post('/user/info', params),
};

export default userApi;