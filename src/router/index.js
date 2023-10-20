import { createRouter, createWebHistory } from 'vue-router';
import { useAuthorityStore } from '@/stores/authority';
import AppointmentHome from '@/views/Home.vue';
import User from '@/views/User.vue';
import UserCenter from '@/views/UserCenter.vue';
import UserEdit from '@/views/UserEdit.vue';
import Appointment from '@/views/Appointment.vue';
import Register from '@/views/Register.vue';
import Login from '@/views/Login.vue';
import AppointmentHistory from '@/views/AppointmentHistory.vue';
import UnfinishedAppointment from '@/views/UnfinishedAppointment.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/', component: AppointmentHome,
      children: [
        { path: '', redirect: 'appointment' },
        { path: 'appointment', component: Appointment },
        {
          path: 'user',
          component: User,
          children: [
            { path: '', component: UserCenter},
            { path: 'edit', component: UserEdit },
            { path: 'register', component: Register },
            { path: 'login', component: Login },
            { path: 'history', component: AppointmentHistory },
            { path: 'mine', component: UnfinishedAppointment },
          ]
        },
      ]
    },
  ]
})

router.beforeEach((to, from, next) => {
  if (to.meta.isAuth) {
    const authorityStore = useAuthorityStore()
    if (authorityStore.authority) {
      next();
    } else {

    }
  } else {
    next();
  }

})

export default router
