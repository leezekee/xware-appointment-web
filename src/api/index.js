import userApi from "./userApi";
import appointmentApi from "./appointmentApi";

const api = {
    auth: userApi,
    appointment: appointmentApi
};

export default api;
