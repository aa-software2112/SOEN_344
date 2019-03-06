/* eslint-disable */
<template>
<div id="app-container">    
    <div id="main-content-area" class="main-color content-fluid">
        <h1>Login as...</h1>
        </br>
        <div class="container reg-container" id="login-select">
        
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
        </div>
    </div>
    
</div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Login',
  methods: {
    
    gotoPatientLogin()
    {
        this.$router.push({path:'/patientLogin'})
    },
    
    gotoNurseLogin()
    {
        this.$router.push({path:'/nurseLogin'})
    },
    
    gotoDoctorLogin()
    {
        this.$router.push({path:'/doctorLogin'})
    },
    
    gotoAdminLogin()
    {
        this.$router.push({path:'/adminLogin'})
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>
</style>
