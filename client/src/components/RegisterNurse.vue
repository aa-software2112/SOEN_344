/* eslint-disable */
<template>
<div id="app-container">    
    <div id="main-content-area" class="main-color content-fluid">
        <h1>Register Nurse</h1>
        <h3 class="error-message">{{fail_message}}</h3>
        <h3 class="success-message">{{success_message}}</h3>
        </br>
        <div class="container reg-container" id="nurse-reg">
            
            <form v-if="canRegisterNurse" @submit="checkForm" class="reg-form" action="">
                
                <div class="form-group">
                    <label for="access_id">Access ID</label>
                    <input type="text" class="form-control" v-model="access_id" name="access_id" id="access_id">
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
                    <label for="password">Password</label>
                    <input type="password" class="form-control" v-model="password" name="password" id="password">
                </div>
                <div class="form-group">
                    <label for="clinic">Clinic</label>
                    <select v-model="clinic_id" name=clinic_id class="form-control" required>
                        <option value="">Select a Clinic</option>
                        <option value v-for="clinic in clinics":value="clinic.id">{{ clinic.name + ", " + clinic.location }}</option>
                    </select>
                </div>
                <button value="submit" type="submit" class="btn btn-default submit">Submit</button>
            </form>
            <h3 v-else-if="notIsAdmin" class="error-message">Must be an Administrator to register a Nurse</h3>
            
            
        
        </div>
    </div>
    
</div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'RegisterNurse',

  data() {
    return {
        access_id: '',
        first_name: '',
        last_name: '',
        password: '',
        nurse_created: false,
        fail_message: '',
        success_message: '',
        clinic_id: '',
        clinics: []
    }
  },
    
    watch: {
        access_id: function(query) {
            this.getClinics();
        },
    },

  methods: {
    checkForm: function(e) {
        e.preventDefault();
        if (!this.access_id || !this.first_name ||
                !this.last_name || !this.password)
        {
            this.message = "Data missing";
            return false;
        }
        this.submitForm();
        return false;
    },
  
    submitForm()
    {   
        axios.put('http://127.0.0.1:5000/nurse', 
        {
            access_id: this.access_id,
            first_name: this.first_name,
            last_name: this.last_name,
            password: this.password
        })
        .then(response => {
        this.nurse_created = true
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
    canRegisterNurse: function()
    {
        return this.nurse_created == false && this.$cookies.get('user_type') == 'admin'
    
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
