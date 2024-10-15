import userApi from "./userApi";
import appointmentApi from "./appointmentApi";
import ResponseCode from "./code";

const api = {
    auth: userApi,
    appointment: appointmentApi,
    code: ResponseCode
};

export default api;
