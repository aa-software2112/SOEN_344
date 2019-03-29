/* eslint-disable */
<template>
<div id="app-container">    
    <div id="main-content-area" class="main-color content-fluid">
        <h1>Register Doctor</h1>
        <h3 class="error-message">{{fail_message}}</h3>
        <h3 class="success-message">{{success_message}}</h3>
        </br>
        <div class="container reg-container" id="doctor-reg">
            
            <form v-if="canRegisterDoctor" @submit="checkForm" class="reg-form" action="">
                
                <div class="form-group">
                    <label for="physician_permit_nb">Physician Permit Number</label>
                    <input type="text" class="form-control" v-model="physician_permit_nb" name="physician_permit_nb" id="physician_permit_nb">
                </div> 
                <div class="form-group">
                    <label for="first_name">First Name</label>
                    <input type="text" class="form-control" v-model="first_name" name="first_name" id="first_name">
                </div> 
                <div class="form-group">
                    <label for="last_name">Last Name</label>
                    <input type="text" class="form-control" v-model="last_name" name="last_name" id="last_name">
                </div>
                <div class="form-group">
                    <label for="city">City</label>
                    <input type="text" class="form-control" v-model="city" name="city" id="city">
                </div>
                <div class="form-group">
                    <label for="specialty">Specialty</label>
                    <input type="text" class="form-control" v-model="specialty" name="specialty" id="specialty">
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
                    <input type="password" class="form-control" v-model="password" name="password" id="password">
                </div>
                
                <button value="submit" type="submit" class="btn btn-default submit">Submit</button>
            </form>
            <h3 v-else-if="notIsAdmin" class="error-message">Must be an Administrator to register a Doctor</h3>
            
            
        
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
        physician_permit_nb: '',
        first_name: '',
        last_name: '',
        city: '',
        specialty: '',
        password: '',
        doctor_created: false,
        fail_message: '',
        success_message: '',
        clinic_id: '',
        clinics: []
    }
  },
      
  watch: {
        physician_permit_nb: function(query) {
            this.getClinics();
        },
  },

  methods: {
    checkForm: function(e) {
        e.preventDefault();
        if (!this.physician_permit_nb || !this.first_name ||
                !this.last_name || !this.city || !this.specialty ||
                !this.password)
        {
            this.message = "Data missing";
            return false;
        }
        this.submitForm();
        return false;
    },
  
    submitForm()
    {   
        axios.put('http://127.0.0.1:5000/doctor', 
        {
            physician_permit_nb: this.physician_permit_nb,
            first_name: this.first_name,
            last_name: this.last_name,
            city: this.city,
            specialty: this.specialty,
            password: this.password
        })
        .then(response => {
        this.doctor_created = true
        this.fail_message = ''
        this.success_message = response.data.message
        console.log(response);
        })
        .catch(error => {
        console.log(error)
        this.fail_message = error.response.data.error.message;
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
  },
  
  computed: 
  {
    canRegisterDoctor: function()
    {
        return this.doctor_created == false && this.$cookies.get('user_type') == 'admin'
    
    },
    
    notIsAdmin: function()
    {
        return !(this.$cookies.get('user_type') == 'admin')
    }
  
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>
#app 
{
    margin: 0;
}

</style>
