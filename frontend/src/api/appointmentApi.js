import {
    http,
    get,
    post,
    del,
    put
} from './axios';

let appointmentApi = {
    getPendingAppointments: () => get('/appointment/pending'),
    getAppointmentList: () => get('/appointment/list'),
    getAppointmentDetail: (id) => get(`/appointment/detail?appointment_id=${id}`),
    cancelAppointment: (id) => del('/appointment', { appointment_id: id }),
    createAppointment: (params) => post('/appointment', params),
    deleteAppointment: (params) => del('/appointment', params),
    getTimeSlot: () => get('/timeslot'),
    getProblemType: () => get('/problem/type'),
};

export default appointmentApi;