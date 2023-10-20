import {
    http,
    get,
    post,
    del,
    put
} from './axios';

let appointmentApi = {
    getAppointmentList: (params) => get('/appointment/list', params),
    getAppointment: (params) => get('/appointment', params),
    getTodoAppointmentSum: (params) => get('/appointment/todo', params),
    getTodoAppointmentSum: (params) => get('/appointment/todo/sum', params),
    createAppointment: (params) => post('/appointment', params),
    updateAppointment: (params) => put('/appointment', params),
    deleteAppointment: (params) => del('/appointment', params),
};

export default appointmentApi;