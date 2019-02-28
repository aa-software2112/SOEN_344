/* eslint-disable */
<template>
<div id="app-container">    
    <div id="main-content-area" class="main-color content-fluid">
        <h1> Register a Doctor/Nurse </h1>
        </br>
        <div class="container reg-container" id="doctor-reg">
            
            <form class="reg-form" action="http://localhost:5000/registerDoctor/" method="put">
                
                <div class="form-group">
                    <label for="physician_permit_nb">Physician Permit Number</label>
                    <input type="text" class="form-control" name="physician_permit_nb" id="physician_permit_nb">
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
                    <label for="city">City</label>
                    <input type="text" class="form-control" name="city" id="city">
                </div>
                <div class="form-group">
                    <label for="specialty">Specialty</label>
                    <input type="text" class="form-control" name="specialty" id="specialty">
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

export default {
  name: 'RegisterDoctor',

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
