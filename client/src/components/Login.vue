/* eslint-disable */
<template>
  <div id="app-container">
    <div id="main-content-area" class="main-color content-fluid">
      <form>
        <h1>Login as...</h1>
        </br>
        <div class="row justify-content-center">
          <a href="" class="login-button" v-on:click="gotoPatientLogin">Patient</a>
        </div>
        <div class="row justify-content-center">
          <a href="" class="login-button" v-on:click="gotoNurseLogin">Nurse</a>
        </div>
        <div class="row justify-content-center">
          <a href="" class="login-button" v-on:click="gotoDoctorLogin">Doctor</a>
        </div>
        <div class="row justify-content-center">
          <a href="" class="login-button" v-on:click="gotoAdminLogin">Administrator</a>
        </div>
      </form>

    </div>

  </div>
</template>

<script>
  import axios from 'axios';

  export default {
    name: 'Login',
    methods: {

      gotoPatientLogin() {
        this.$router.push({path: '/login/patient'})
      },

      gotoNurseLogin() {
        this.$router.push({path: '/login/nurse'})
      },

      gotoDoctorLogin() {
        this.$router.push({path: '/login/doctor'})
      },

      gotoAdminLogin() {
        this.$router.push({path: '/login/admin'})
      }
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>
</style>
