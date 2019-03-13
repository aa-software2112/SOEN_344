/* eslint-disable */
<template>
  <div>
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
      <div class="logo">
      </div>
      <div class="navbar-header">
        <a class="navbar-brand" href="/">Home</a>
      </div>

      <div class="container justify-content-end navbar-right">

        <div class="row justify-content-end">
            <!-- Any logged user -->
            <div v-if="isLogged">
                <a class="navbar-brand" href="#" v-on:click="logout">Logout</a>
            </div>
            
            <!-- Any non-logged user -->
            <div v-if="notLoggedOrNoCookiesSet">
                <a class="navbar-brand" href="/registerPatient">Register</a>
                <a class="navbar-brand" href="/login">Login</a>
            </div>
            
            <!-- A logged in Patient -->
            <div v-if="loggedPatient">
                <a class="navbar-brand" href="/bookingsViewer">My Bookings</a>
                <a class="navbar-brand" href="/cart">Cart</a>
                <a class="navbar-brand" href="/schedule">Schedule Appointment</a>
            </div>
                
            <!-- A logged in Admin -->
            <div v-if="isLoggedAdmin">
                <a class="navbar-brand" href="/adminRegistrationMenu">Registration Menu</a>
            </div>
            
            <!-- A logged in Doctor -->
            <div v-if="isLoggedDoctor">
                <a class="navbar-brand" href="/createAvailability">Create Availability</a>
                <a class="navbar-brand" href="/viewAvailability">Manage Availability</a>
            </div>
            
            <!-- A logged in Nurse -->
            <div v-if="isLoggedNurse">
                <a class="navbar-brand" href="/schedule">Schedule Appointment</a>
                <a class="navbar-brand" href="/nurse/viewBooking">Booking System</a>
            </div>
            
            <!-- Unknown -->
            <a class="navbar-brand" href="/appointment">Appointment</a>
        </div>
      </div>

    </nav>
  </div>
</template>


<script>
  import axios from 'axios';

  export default {
    name: 'Navbar',
    methods: {
      logout(e) {
        e.preventDefault();
        const p = 'http://127.0.0.1:5000/logout';

        axios.get(p)
          .then(response => {
            this.$router.push({path: '/'});
            location.reload();
            //this.message = response.data.message + response.headers["set-cookie"];
            console.log(response);
          })
          .catch(error => {
            console.log(error)
            this.message = error.response.data.error.message;
          })
      }

    },

    computed: {

      notLoggedPatient: function () {
        return !(this.$cookies.get('logged') == 'True' && this.$cookies.get('user_type') == 'patient')
      },

      loggedPatient: function () {
        return (this.$cookies.get('logged') == 'True' && this.$cookies.get('user_type') == 'patient')
      },
      notLoggedOrNoCookiesSet: function () {
        return this.$cookies.get('logged') == 'False' || this.$cookies.get('logged') == null

      },

      notLogged: function () {
        return this.$cookies.get('logged') == 'False'
      },
      isLogged: function () {
        return this.$cookies.get('logged') == 'True'
      },
      isLoggedAdmin: function () {
        return this.$cookies.get('logged') == 'True' && this.$cookies.get('user_type') == 'admin'

      },
      isLoggedDoctor: function () {
        return this.$cookies.get('logged') == 'True' && this.$cookies.get('user_type') == 'doctor'

      },
      isLoggedNurse: function () {
        return this.$cookies.get('logged') == 'True' && this.$cookies.get('user_type') == 'nurse'

      }

    }

  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>
  #app {
    margin: 0;
  }

  .navbar-brand {
    color: #f2f2f2 !important;
    text-align: center;
    padding: 14px 14px;
    text-decoration: none;
  }

  .navbar {
    background-color: #333 !important;
    overflow: hidden;
    border-radius: 5px;

  }

  .navbar-right {
    position: absolute;
    right: 0px;
  }

</style>
