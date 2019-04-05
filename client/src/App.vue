/* eslint-disable */
<template>
  <div id="app">
    <div class="homepage-image"></div>

    <div class="homepage">
      <navbar></navbar>
      <router-view/>
    </div>

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
