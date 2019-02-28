import Vue from 'vue';
import Router from 'vue-router';
import Home from '@/components/Home'
import Navbar from '@/components/Navbar';
import Register from '@/components/Register';
import Cart from '@/components/Cart'
import Schedule from '@/components/Schedule'
import RegisterDoctor from '@/components/RegisterDoctor';
import axios from 'axios';
import * as Cookies from 'js-cookie';

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
      path: '/register',
      name: 'Register',
      component: Register
    },
    {
      path: '/cart',
      name: 'Cart',
      component: Cart
    },
    {
      path: '/schedule',
      name: 'Schedule',
      component: Schedule
    },
    {
      path: '/registerDoctor',
      name: 'RegisterDoctor',
      component: RegisterDoctor
    }
  ]
});
