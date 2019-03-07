/* eslint-disable */
<template>
<div id="app-container">    
    <div id="main-content-area" class="main-color content-fluid">
        <h1>Doctor Login</h1>
        
        <h3 class="error-message">{{message}}</h3>
        </br>
        <div class="container reg-container" id="patient-reg">
            
            <form @submit="submitForm" class="reg-form" action="" >
                
                <div class="form-group">
                    <label for="physician_permit">Physician Permit</label>
                    <input type="text" class="form-control" v-model="physician_permit" id="physician_permit">
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
  name: 'DoctorLogin',

  data () {
  return {
    physician_permit : '',
    password : '',
    message: ''
    }
  },
  
  
  methods: {
    
    submitForm(e)
    {   
        e.preventDefault();
        const p = 'http://127.0.0.1:5000/loginDoctor';
        
        axios.post(p, 
        {
            physician_permit : this.physician_permit,
            password : this.password
        })
        .then(response => {
        this.$router.go({path:"/"});
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
