import {
    http,
    get,
    post,
    del,
    put
} from './axios';

let userApi = {
    login: (params) => post('/auth/login', params),
    register: (params) => post('/auth/register', params),
    logout: () => get('/auth/logout'),
    getUserInfo: () => get('/auth/info'),
    updateUserInfo: (params) => put('/auth/info', params),
};

export default userApi;