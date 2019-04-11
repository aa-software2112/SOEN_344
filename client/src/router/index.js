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
import AdminManageClinics from '@/components/AdminManageClinics';
import ViewAvailability from '@/components/ViewAvailability';
import NurseViewBooking from '@/components/NurseViewBooking';
import BookingsViewer from '@/components/BookingsViewer';
import PatientSearch from '@/components/PatientSearch';
import DoctorSearch from '@/components/DoctorSearch';
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
      path: '/schedule',
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
      path: '/login/patient',
      name: 'PatientLogin',
      component: PatientLogin
    },
    {
      path: '/login/nurse',
      name: 'NurseLogin',
      component: NurseLogin
    },
    {
      path: '/login/doctor',
      name: 'DoctorLogin',
      component: DoctorLogin
    },
    {
      path: '/login/admin',
      name: 'AdminLogin',
      component: AdminLogin
    },
    {
      path: '/adminRegistrationMenu',
      name: 'AdminRegistrationMenu',
      component: AdminRegistrationMenu
    },
    {
      path: '/adminManageClinics',
      name: 'AdminManageClinics',
      component: AdminManageClinics
    },
    {
      path: '/viewAvailability',
      name: 'ViewAvailability',
      component: ViewAvailability
    },
    {
      path: '/nurse/viewBooking',
      name: 'NurseViewBooking',
      component: NurseViewBooking
    },
    {
        path: '/bookingsViewer/:id',
        name: 'BookingsViewer',
        component: BookingsViewer
    },
    {
        path: '/bookingsViewer/doctor/:id',
        name: 'BookingsViewer',
        component: BookingsViewer
    },
    {
        path: '/bookingsViewer',
        name: 'BookingsViewer',
        component: BookingsViewer
        
    }
    
  ]
});
