/* eslint-disable */
<template>
  <div id="app" class="homepage">

    <navbar></navbar>
    <router-view/>
  </div>
</template>

<script>
import Navbar from '@/components/Navbar';

export default {
  name: "App",
  
  components: {
    'navbar': Navbar
  },
};
</script>

<style>

</style>
