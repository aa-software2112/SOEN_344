/* eslint-disable */
<template>
<div id="app-container">    
    <div id="main-content-area" class="main-color content-fluid">
        <h1>Patient Login</h1>
        
        <h3 class="error-message">{{message}}</h3>
        </br>
        <div class="container reg-container" id="patient-reg">
            
            <form @submit="submitForm" class="reg-form" action="" >
                
                <div class="form-group">
                    <label for="health_card_nb">Health Card Number</label>
                    <input type="text" class="form-control" v-model="health_card_nb" id="health_card_nb">
                </div>
                <div class="form-group">
                    <label for="password">Password</label>
                    <input minlength="1" type="password" class="form-control" v-model="password" id="password">
                </div>
                
                <button value="submit" type="submit" class="btn btn-default submit">Submit</button>
            
            </form>
           
        </div>
    </div>
    
</div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'PatientLogin',

  data () {
  return {
    health_card_nb : '',
    password : '',
    message: ''
    }
  },
  
  
  methods: {
    
    submitForm(e)
    {   
        e.preventDefault();
        const p = 'http://127.0.0.1:5000/login';
        
        axios.post(p, 
        {
            health_card_nb : this.health_card_nb,
            password : this.password
        })
        .then(response => {
        this.$router.push({path:"/"});
        //this.message = response.data.message + response.headers["set-cookie"];
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
