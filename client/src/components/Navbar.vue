/* eslint-disable */
<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-light">

    <div class="logo">
    </div>

    <ul>
      <li v-if="isLogged">
        <a class="navbar-brand" href="/" v-for="clinic in current_clinic">
          {{clinic.name }}</a>
      </li>
      <li v-if="notLoggedOrNoCookiesSet">
        <a class="navbar-brand" href="/">Home</a>
      </li>
      <li v-if="isLoggedAdmin">
        <a class="navbar-brand" href="/">Home</a>
      </li>
    </ul>

    <ul class="row justify-content-end navbar-right">

      <!-- Any non-logged user -->
      <div v-if="notLoggedOrNoCookiesSet">
        <li>
          <a class="navbar-brand" href="/registerPatient">Register</a>
        </li>
        <li>
          <a class="navbar-brand" href="/login">Login</a>
        </li>
      </div>

      <!-- A logged in Patient -->
      <div v-if="loggedPatient">
        <li>
          <a class="navbar-brand" href="/bookingsViewer">My Bookings</a>
        </li>
        <li>
          <a class="navbar-brand" href="/cart">Cart</a>
        </li>
        <li>
          <a class="navbar-brand" href="/schedule">Schedule Appointment</a>
        </li>
      </div>

      <!-- A logged in Admin -->
      <li v-if="isLoggedAdmin">
        <a class="navbar-brand" href="/adminRegistrationMenu">Registration Menu</a>
      </li>

      <!-- A logged in Doctor -->
      <div v-if="isLoggedDoctor">
        <li>
          <a class="navbar-brand" href="/createAvailability">Create Availability</a>
        </li>
        <li>
          <a class="navbar-brand" href="/viewAvailability">Manage Availability</a>
        </li>
      </div>

      <!-- A logged in Nurse -->
      <div v-if="isLoggedNurse">
        <li>
          <a class="navbar-brand" href="/schedule">Schedule Appointment</a>
        </li>
        <li>
          <a class="navbar-brand" href="/nurse/viewBooking">Booking System</a>
        </li>
      </div>

      <!-- Any logged user -->
      <li v-if="isLogged">
        <a class="navbar-brand logout" href="#" v-on:click="logout">Logout</a>
      </li>

      <!-- Unknown -->
      <!--<a class="navbar-brand" href="/appointment">Appointment</a>-->
    </ul>

  </nav>
</template>


<script>
  import axios from 'axios';

  export default {
    name: 'Navbar',
    data() {
      return {
        msg: "Welcome to UberSante",
        current_clinic: null,
      };
    },

    created() {
      this.setCurrentClinic();
    },

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
      },
      setCurrentClinic: function () {
        axios.get('http://127.0.0.1:5000/clinic/' + this.$cookies.get('user_type') + '/' + this.$cookies.get('id'), {}).then(response => {
          this.current_clinic = response.data.data
        })
          .catch(error => {
            console.log(error)
            this.message = error.response.data.error.message;
          })
      },
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

</style>
