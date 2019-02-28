import Vue from 'vue';
import Router from 'vue-router';
import Ping from '@/components/Ping';
import Navbar from '@/components/Navbar';
import axios from 'axios';
import * as Cookies from 'js-cookie';

Vue.use(Router);

Vue.prototype.$cookies = Cookies;

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      name: 'Ping',
      component: Ping
    },
    {
      path: '/nav',
      name: 'Navbar',
      component: Navbar
    }
  ]
});
