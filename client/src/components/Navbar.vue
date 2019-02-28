/* eslint-disable */
<template>
<div>
<nav class="navbar navbar-expand-lg navbar-light bg-light">
    <div class="navbar-header">
      <a class="navbar-brand" href="/">UberSante</a>
    </div>
    <div class="navbar-right">
    <a class="navbar-brand" href="/Register" v-if="this.$cookies.get('logged') == 'False' || !this.$cookies">Register</a>
    <a class="navbar-brand" href="#" v-if="this.$cookies.get('logged') == 'True' && this.$cookies.get('user_type') == 'admin'">Register Doctor/Nurse</a>
    <a class="navbar-brand" href="/Login" v-if="this.$cookies.get('logged') == 'False' || !this.$cookies">Login</a>
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
  float: right;
}

</style>
