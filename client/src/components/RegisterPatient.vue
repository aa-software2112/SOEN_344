/* eslint-disable */
<template>
<div id="app-container">    
    <div id="main-content-area" class="main-color content-fluid">
        <h1>Register a Patient</h1>
        <h3 class="error-message">{{message}}</h3>
        </br>
        <div class="container reg-container" id="patient-reg">
            
            <form @submit="checkForm" class="reg-form" action="" >
                
                <div class="form-group">
                    <label for="health_card_nb">Health Card Number</label>
                    <input minlength="12" maxlength="12" type="text" class="form-control" v-model="health_card_nb" id="health_card_nb">
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
                    <label for="date_of_birth">Date of Birth</label>
                    <input type="date" class="form-control" v-model="date_of_birth" id="date_of_birth">
                </div>
                <div class="form-group">
                    <label for="gender">Gender</label>
                    <select id="gender" v-model="gender" class="form-control" required>
                        <option value="">Select Gender</option>
                        <option value="M">Male</option>
                        <option value="F">Female</option>
                    </select>
                </div>
                <div class="form-group">
                    <label for="phone_nb">Phone Number</label>
                    <input minlength="10" maxlength="10" type="tel" class="form-control" v-model="phone_nb" id="phone_nb">
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
                    <label for="clinic">Clinic</label>
                    <select v-model="clinic_id" name=clinic_id class="form-control" required>
                        <option value="">Select a Clinic</option>
                        <option value v-for="clinic in clinics":value="clinic.id">{{ clinic.name + ", " + clinic.location }}</option>
                    </select>
                </div>
                <div class="form-group">
                    <label for="password">Password</label>
                    <input minlength="6" type="password" class="form-control" v-model="password" id="password">
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
  name: 'RegisterPatient',

  data () {
  return {
    health_card_nb : '',
    date_of_birth : 'yyyy-mm-dd',
    gender : '',
    phone_nb : '',
    home_address : '',
    email : '',
    first_name : '',
    last_name : '',
    password : '',
    message : '',
    clinic_id : '',
    clinics : [],
    }
  },
      
    watch: {
        gender: function(query) {
            this.getClinics();
        },
    },

  methods: {
    checkForm: function(e) {
        e.preventDefault();
        if (!this.health_card_nb || !this.date_of_birth ||
                !this.gender || !this.phone_nb || !this.home_address ||
                !this.email || !this.first_name || !this.last_name || 
                !this.password || !this.clinic_id)
        {
            this.message = "Data missing";
            return false;
        }
        this.submitForm();
        return false;
    },
  
    submitForm()
    {   
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
            password : this.password,
            clinic_id: this.clinic_id
        })
        .then(response => {
        this.$router.push({path:"/login"});
        console.log(response);
        })
        .catch(error => {
        console.log(error)
        this.message = error.response.data.error.message;
        })
    },

    getClinics: function() {
        axios.get('http://127.0.0.1:5000/clinic', {
        }).then(response => {
                this.clinics = response.data.data
            })
            .catch(error => {
                console.log(error)
                this.message = error.response.data.error.message;
            })
      },

  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>
</style>
