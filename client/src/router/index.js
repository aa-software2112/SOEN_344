import Vue from 'vue';
import Router from 'vue-router';
import Home from '@/components/Home'
import Navbar from '@/components/Navbar';
import RegisterPatient from '@/components/RegisterPatient';
import Cart from '@/components/Cart'
import SearchAppointment from '@/components/SearchAppointment'
import CreateAvailability from '@/components/CreateAvailability'
import RegisterDoctor from '@/components/RegisterDoctor';
import RegisterNurse from '@/components/RegisterNurse';
import Login from '@/components/Login';
import PatientLogin from '@/components/PatientLogin';
import NurseLogin from '@/components/NurseLogin';
import DoctorLogin from '@/components/DoctorLogin';
import AdminLogin from '@/components/AdminLogin';
import AdminRegistrationMenu from '@/components/AdminRegistrationMenu';
import axios from 'axios';
import * as Cookies from 'js-cookie';
axios.defaults.withCredentials = true;
Vue.use(Router);

Vue.prototype.$cookies = Cookies;


export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      name: 'Home',
      component: Home
    },
    {
      path: '/nav',
      name: 'Navbar',
      component: Navbar
    },
    {
      path: '/registerPatient',
      name: 'RegisterPatient',
      component: RegisterPatient
    },
    {
      path: '/cart',
      name: 'Cart',
      component: Cart
    },
    {
      path: '/searchAppointment',
      name: 'SearchAppointment',
      component: SearchAppointment
    },
    {
      path: '/registerDoctor',
      name: 'RegisterDoctor',
      component: RegisterDoctor
    },
    {
      path: '/registerNurse',
      name: 'RegisterNurse',
      component: RegisterNurse
    },
    {
      path: '/createAvailability',
      name: 'CreateAvailability',
      component: CreateAvailability
    },
    {
      path: '/login',
      name: 'Login',
      component: Login
    },
    {
      path: '/patientLogin',
      name: 'PatientLogin',
      component: PatientLogin
    },
    {
      path: '/nurseLogin',
      name: 'NurseLogin',
      component: NurseLogin
    },
    {
      path: '/doctorLogin',
      name: 'DoctorLogin',
      component: DoctorLogin
    },
    {
      path: '/adminLogin',
      name: 'AdminLogin',
      component: AdminLogin
    },
    {
      path: '/adminRegistrationMenu',
      name: 'AdminRegistrationMenu',
      component: AdminRegistrationMenu
    }
  ]
});
