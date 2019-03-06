/* eslint-disable */
<template>
<div>
<nav class="navbar navbar-expand-lg navbar-light bg-light">
  <div class="logo">
  </div>
    <div class="navbar-header">
      <a class="navbar-brand" href="/">Home</a>
    </div>
    <div class="navbar-right">
    <a class="navbar-brand" href="/register" v-if="notLoggedPatient">Register</a>
    <a class="navbar-brand" href="/login" v-if="notLoggedPatient">Login</a>
    <a class="navbar-brand" href="#" v-on:click="logout" v-if="isLogged">Logout</a>
    
    <!-- Admin Tabs -->
    <a class="navbar-brand" href="/registerDoctor" v-if="this.$cookies.get('logged') == 'True' && this.$cookies.get('user_type') == 'admin'">Register Doctor/Nurse</a>
    <a class="navbar-brand" href="/createAvailability" v-if="this.$cookies.get('logged') == 'True' && this.$cookies.get('user_type') == 'admin'">Make Availability</a>

    
    <!-- Patient Tabs-->
    <a class="navbar-brand" href="/cart" v-if="this.$cookies.get('logged') == 'True'">Cart</a>
    <a class="navbar-brand" href="/schedule" v-if="this.$cookies.get('logged') == 'True'">Schedule Appointment</a>
    <a class="navbar-brand" href="/appointment" v-if="this.$cookies.get('logged') == 'True'">Appointment</a>
    </div>
    
</nav>
</div>
</template>


<script>
import axios from 'axios';

export default {
  name: 'Navbar',
  methods : {
    logout(e)
    {
        e.preventDefault();
        const p = 'http://127.0.0.1:5000/logout';
        
        axios.get(p)
        .then(response => {
        this.$router.go({path:"/"});
        //this.message = response.data.message + response.headers["set-cookie"];
        console.log(response);
        })
        .catch(error => {
        console.log(error)
        this.message = error.response.data.error.message;
        })
    }
  
  },
  
  computed:{
    
    notLoggedPatient: function()
    {
        return !(this.$cookies.get('logged') == 'True' && this.$cookies.get('user_type') == 'patient')
    },
    
    isLogged: function()
    {
        return this.$cookies.get('logged') == 'True'
    }
    
    }

}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>
#app 
{
    margin: 0;
}

.navbar-brand {
  color: #f2f2f2 !important;
  text-align: center;
  padding: 14px 14px;
  text-decoration: none;
}

.navbar {
  background-color: #333 !important;
  overflow: hidden;
}

.navbar-right{
 position:absolute; 
 right:0px; 
}

</style>
