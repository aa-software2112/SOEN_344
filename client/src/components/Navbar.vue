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
    <a class="navbar-brand" href="/register" v-if="this.$cookies.get('logged') == 'False' || !this.$cookies.isSet">Register</a>
    <a class="navbar-brand" href="/registerDoctor" v-if="this.$cookies.get('logged') == 'True' && this.$cookies.get('user_type') == 'admin'">Register Doctor/Nurse</a>
    <a class="navbar-brand" href="/login" v-if="this.$cookies.get('logged') == 'False' || !this.$cookies.isSet">Login</a>
    
    <!-- Patient Tabs-->
    <a class="navbar-brand" href="/cart" v-if="this.$cookies.get('logged') == 'True' || !this.$cookies">Cart</a>
    <a class="navbar-brand" href="/schedule" v-if="this.$cookies.get('logged') == 'True' || !this.$cookies">Schedule Appointment</a>
    <a class="navbar-brand" href="/appointment" v-if="this.$cookies.get('logged') == 'True' || !this.$cookies">Appointment</a>
    </div>
</nav>
</div>
</template>

<script>
import axios from 'axios'
 

export default {
  name: 'Navbar'
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
