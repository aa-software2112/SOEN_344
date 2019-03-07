/* eslint-disable */
<template>
  <div id="app-container">
    <div id="main-content-area" class="main-color content-fluid">

      <form @submit="submitForm" class="reg-form" action="">
        <h1>Admin Login</h1>
        <h3 class="error-message">{{message}}</h3>
        </br>
        <div class="form-group">
          <label for="health_card_nb">Email</label>
          <input type="email" class="form-control" v-model="email" id="email">
        </div>
        <div class="form-group">
          <label for="password">Password</label>
          <input minlength="1" type="password" class="form-control" v-model="password" id="password">
        </div>

        <button value="submit" type="submit" class="btn btn-default submit">Submit</button>

      </form>
    </div>

  </div>
</template>

<script>
  import axios from 'axios';

  export default {
    name: 'AdminLogin',

    data() {
      return {
        email: '',
        password: '',
        message: ''
      }
    },


    methods: {

      submitForm(e) {
        e.preventDefault();
        const p = 'http://127.0.0.1:5000/loginAdmin';

        axios.post(p,
          {
            email: this.email,
            password: this.password
          })
          .then(response => {
            this.$router.push({path: "/"});
            location.reload();
            console.log(response);
          })
          .catch(error => {
            console.log(error)
            this.message = error.response.data.error.message;
          })

      }
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>
</style>
