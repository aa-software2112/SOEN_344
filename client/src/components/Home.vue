/* eslint-disable */
<template>
  <div class="main">
    <div class='page-main'>
       <h1>
         {{ msg }}
         </h1>
    </div>
    
  </div>
</template>

<script>
export default {
  name: 'Home',
  data() {
    return {
      msg: "Welcome to UberSante"
    };
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
