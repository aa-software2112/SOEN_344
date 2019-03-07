/* eslint-disable */
<template>
<div id="app-container">    
    <div id="main-content-area" class="main-color content-fluid">
        <h1>Nurse Login</h1>
        
        <h3 class="error-message">{{message}}</h3>
        </br>
        <div class="container reg-container" id="patient-reg">
            
            <form @submit="submitForm" class="reg-form" action="" >
                
                <div class="form-group">
                    <label for="access_id">Access ID</label>
                    <input type="text" class="form-control" v-model="access_id" id="access_id">
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
  name: 'NurseLogin',

  data () {
  return {
    access_id : '',
    password : '',
    message: ''
    }
  },
  
  
  methods: {
    
    submitForm(e)
    {   
        e.preventDefault();
        const p = 'http://127.0.0.1:5000/loginNurse';
        
        axios.post(p, 
        {
            access_id : this.access_id,
            password : this.password
        })
        .then(response => {
        this.$router.push({path:"/"});
        location.reload();
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
