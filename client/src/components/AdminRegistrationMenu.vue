/* eslint-disable */
<template>
<div id="app-container">    
    <div id="main-content-area" class="main-color content-fluid">
        <h1>Register a...</h1>
        </br>
        <div class="container reg-container" id="login-select">
        
            <div class="row justify-content-center">
                <a href="" class="register-menu-button" v-on:click="gotoDoctorRegistration">Doctor</a>
            </div>
            <div class="row justify-content-center">
                <a href="" class="register-menu-button" v-on:click="gotoNurseRegistration">Nurse</a>
            </div>
        </div>
    </div>
    
</div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'AdminRegistrationMenu',
  methods: {
    
    gotoDoctorRegistration()
    {
        this.$router.push({path:'/registerDoctor'})
    },
    
    gotoNurseRegistration()
    {
        this.$router.push({path:'/registerNurse'})
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>
</style>
