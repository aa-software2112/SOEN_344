/* eslint-disable */
<template>
<div id="app-container">
    <Navbar></Navbar>
    
    <div id="main-content-area" class="main-color content-fluid">
        <h1> Register as Patient </h1>
        </br>
        <div class="container reg-container" id="patient-reg">
            
            <form class="reg-form" action="http://localhost:5000/patient/" method="put">
                
                <div class="form-group">
                    <label for="health_card_nb">Health Card Number</label>
                    <input type="text" class="form-control" name="health_card_nb" id="health_card_nb">
                </div> 
                <div class="form-group">
                    <label for="date_of_birth">Date of Birth</label>
                    <input type="date" class="form-control" name="date_of_birth" id="date_of_birth">
                </div>
                <div class="form-group">
                    <label for="gender">Gender</label>
                    <select id="gender" name="gender">
                        <option value="M">Male</option>
                        <option value="F">Female</option>
                    </select>
                </div>
                <div class="form-group">
                    <label for="phone_nb">Phone Number</label>
                    <input type="tel" class="form-control" name="phone_nb" id="phone_nb">
                </div>
                <div class="form-group">
                    <label for="home_address">Home Address</label>
                    <input type="text" class="form-control" name="home_address" id="home_address">
                </div>
                <div class="form-group">
                    <label for="email">Email</label>
                    <input type="email" class="form-control" name="email" id="email">
                </div>
                <div class="form-group">
                    <label for="first_name">First Name</label>
                    <input type="text" class="form-control" name="first_name" id="first_name">
                </div> 
                <div class="form-group">
                    <label for="last_name">Last Name</label>
                    <input type="text" class="form-control" name="last_name" id="last_name">
                </div>
                <div class="form-group">
                    <label for="password">Password</label>
                    <input type="password" class="form-control" name="password" id="password">
                </div>
                
                <button @click.prevent="getFormValues()" type="submit" class="btn btn-default submit">Submit</button>
            
            </form>
           
        
        </div>
    </div>
    
</div>
</template>

<script>
import axios from 'axios'
import Navbar from './Navbar'

export default {
  name: 'Register',
  components: {
    'Navbar': Navbar
  },
  data() {
    return {
        info: null
    
    }
  },
  
  methods: {
    getFormValues()
    {
        /* Do something to extract values and send a "PUT"... */
    
    
    
    }
  }
  
  /*
  methods: {
   
    getResponse() {
       axios
       .post('http://localhost:5000/login', {health_card_nb:'XGCB 1090 0810', password:'password'}, 
            { headers: {'Content-Type': 'application/x-www-form-urlencoded'}})
      .then(response => {this.info = response;
      console.log(response);
      })
      .catch(error => {
      this.info = error;
    })
    }
    
  },
  created() {
    this.getResponse()  
  }
 */
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>
#app 
{
    margin: 0;
}

</style>
