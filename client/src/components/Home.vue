/* eslint-disable */
<template>
  <div class="main">
    <div class='page-main'>
       <h1>
         {{ msg }}
       </h1>
      <p v-for="msg in loginMsgList">{{msg.toString()}}</p>
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
          this.loginMsgList = res.data;
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
<style scoped>
h1,
h2 {
  font-weight: normal;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}

.page-main {
  padding: 10px;
}
</style>
