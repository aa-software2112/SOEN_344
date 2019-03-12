/* eslint-disable */
<template>
  <div class="container reg-container home">
    <div id="main-content-area" class="container-fluid ">
      <h1>
        Welcome to UberSante
      </h1>
      <p v-for="loginMsg in loginMsgList">{{ loginMsg }}</p>

    </div>

  </div>
</template>

<script>

import axios from "axios";
export default {
  name: 'Home',
  data() {
    return {
      msg: "Welcome to UberSante",
      loginMsgList: null
    };
  },
  methods: {
    getLoginMessage() {
      const path = "http://127.0.0.1:5000/my-update";
      if (this.$cookies.get('logged') == 'True' && this.$cookies.get('user_type') == 'patient'){
        axios
        .get(path)
        .then(res => {
          this.loginMsgList = res.data.data;
          console.log(res)
        })
        .catch(error => {
          // eslint-disable-next-line
          console.error(error);
        });
      }
      else {
        console.log("no cookie")
      }
    }
  },

  created() {
    this.getLoginMessage();
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>

</style>
