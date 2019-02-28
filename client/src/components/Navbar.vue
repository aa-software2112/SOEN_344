/* eslint-disable */
<template>
<div>
<nav class="navbar navbar-expand-lg navbar-light bg-light">
    <div class="navbar-header">
      <a class="navbar-brand" href="#">UberSante</a>
    </div>
    <a class="navbar-brand" href="#">Home</a>
    <a class="navbar-brand" href="/Register" v-if="this.$cookies.get('logged') == 'False' || !this.$cookies">Register</a>
    <a class="navbar-brand" href="#" v-if="this.$cookies.get('logged') == 'True' && this.$cookies.get('user_type') == 'admin'">Register Doctor/Nurse</a>
    <a class="navbar-brand" href="#" v-if="this.$cookies.get('logged') == 'False' || !this.$cookies">Login</a>
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

</style>
