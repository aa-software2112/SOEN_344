/* eslint-disable */
<template>
<div id="app-container">    
    <div id="main-content-area" class="main-color content-fluid">
        <h1> Make Doctor Availability </h1>
        </br>
        <div class="container reg-container" id="patient-reg">
            
            <form id="form-availability" @submit.prevent="processForm">
                <div class="form-group">
                    <label for="start">Start</label>
                    <input type="text" class="input" name="start" v-model="start">
                </div> 
                <div class="form-group">
                    <label for="room">Room</label>
                    <input type="text" class="input" name="room" v-model="room">
                </div>
                <div class="form-group">
                    <label for="year">Year</label>
                    <input type="text" class="input" name="year" v-model="year">
                </div>
                <div class="form-group">
                    <label for="month">Month</label>
                    <input type="text" class="input" name="month" v-model="month">
                </div>
                 <div class="form-group">
                    <label for="day">Day</label>
                    <input type="text" class="input" name="day" v-model="day">
                </div>
                <div class="form-group">
                <label for="booking_type">Availability Type</label>
                    <select v-model="booking_type" name="book_type">
                        <option value="ANNUAL">Annual</option>
                        <option value="WALKIN">Walkin</option>
                    </select>
                </div>
                <button type="submit" class="btn btn-default submit">Submit</button>
            </form>
           
        
        </div>
    </div>
    
</div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'Register',

  data() {
    return {
        start: '',
        room: '',
        year: '',
        month: '',
        day: '',
        booking_type: '',
        doctor_id: '02'
    }
  },
  
  methods: {
     processForm: function () {
       alert("Creating Availability");
      axios.put('http://localhost:5000/availability', {
          start: this.start,
          room: this.room,
          year: this.year,
          month: this.month,
          day: this.day,
          booking_type: this.booking_type,
          doctor_id: this.doctor_id})
        .then(function (response) {
          console.log(JSON.stringify(response));})
        .catch(function (error) {
          alert(error);
        });
    } 
  }

  }

</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>

</style>
