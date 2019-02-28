/* eslint-disable */
<template>
<div id="app-container">    
    <div id="main-content-area" class="main-color content-fluid">
        <h1> Register as Patient </h1>
        <h3 class="error-message">{{message}}</h3>
        </br>
        <div class="container reg-container" id="patient-reg">
            
            <form @submit="checkForm" class="reg-form" action="" >
                
                <div class="form-group">
                    <label for="health_card_nb">Health Card Number</label>
                    <input type="text" class="form-control" v-model="health_card_nb" id="health_card_nb">
                </div> 
                <div class="form-group">
                    <label for="date_of_birth">Date of Birth</label>
                    <input type="date" class="form-control" v-model="date_of_birth" id="date_of_birth">
                </div>
                <div class="form-group">
                    <label for="gender">Gender</label>
                    <select id="gender" v-model="gender">
                        <option value="M">Male</option>
                        <option value="F">Female</option>
                    </select>
                </div>
                <div class="form-group">
                    <label for="phone_nb">Phone Number</label>
                    <input type="tel" class="form-control" v-model="phone_nb" id="phone_nb">
                </div>
                <div class="form-group">
                    <label for="home_address">Home Address</label>
                    <input type="text" class="form-control" v-model="home_address" id="home_address">
                </div>
                <div class="form-group">
                    <label for="email">Email</label>
                    <input type="email" class="form-control" v-model="email" id="email">
                </div>
                <div class="form-group">
                    <label for="first_name">First Name</label>
                    <input type="text" class="form-control" v-model="first_name" id="first_name">
                </div> 
                <div class="form-group">
                    <label for="last_name">Last Name</label>
                    <input type="text" class="form-control" v-model="last_name" id="last_name">
                </div>
                <div class="form-group">
                    <label for="password">Password</label>
                    <input type="password" class="form-control" v-model="password" id="password">
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
  name: 'Register',

  data () {
  return {
    health_card_nb : '',
    date_of_birth : 'yyyy-mm-dd',
    gender : 'M',
    phone_nb : '',
    home_address : '',
    email : '',
    first_name : '',
    last_name : '',
    password : '',
    message : ''
    }
  },
  
  
  methods: {
    checkForm: function(e) {
        if (!this.health_card_nb || !this.date_of_birth ||
                !this.gender || !this.phone_nb || !this.home_address ||
                !this.email || !this.first_name || !this.last_name || 
                !this.password)
        {
            e.preventDefault();
            this.message = "Data missing";
            return false;
        }
        
        this.submitForm();
        return true;
    },
  
    submitForm()
    {   
        console.log(this.data);
        axios.put('http://localhost:5000/patient', 
        {
        health_card_nb : this.health_card_nb,
        date_of_birth : this.date_of_birth,
        gender : this.gender,
        phone_nb : this.phone_nb,
        home_address : this.home_address,
        email : this.email,
        first_name : this.first_name,
        last_name : this.last_name,
        password : this.password
        }, 
        { headers: {'Content-Type': 'application/x-www-form-urlencoded'}})
        .then(response => {this.message = response;
        console.log(response);
        })
        .catch(error => {
        this.message = error;
        })
    
    }
  }
  
  /*
  methods: {
   
    getResponse() {
       axios
       .post('http://localhost:5000/patient/', data, 
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
