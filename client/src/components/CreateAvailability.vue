/* eslint-disable */
<template>
  <div id="app-container">
    <div id="main-content-area" class="main-color content-fluid">
      <form id="form-availability" class="form" @submit.prevent="processForm">
        <h1> Make Doctor Availability </h1>
        <h3 class="error-message">{{message}}</h3>
        <div class="form-group">
          <label for="booking_type">Availability Type</label>
          <select v-model="booking_type" name="book_type" required>
            <option value="">Select an Availability Type</option>
            <option value="ANNUAL">Annual</option>
            <option value="WALKIN">Walkin</option>
          </select>
        </div>
        <div class="form-group">
          <label for="start">Appointment Time</label>
          <input v-if="booking_type === 'WALKIN'" type="time" value="09:00" min="9:00" max="16:00" step="1200"
                 v-model="start" required>
          <input v-else type="time" value="09:00" min="9:00" max="16:00" step="3600" v-model="start" required>
          <br>
          <span class="help-text">Appointment times are from 9:00am to 4:00pm</span>
        </div>
        <div class="form-group">
          <label for="date">Date</label>
          <input type="Date" class="input" name="date" v-model="date" required>
        </div>
        <div class="form-group">
          <label for="room">Room</label>
          <select v-model="room" name="room" required>
            <option v-if="response.lenth == 0">No rooms available</option>
            <option value="">Select a Room</option>
            <option value v-for="(key, value) in response":value="key">{{ key }}</option>
          </select>
        </div>
        <button type="submit" class="btn btn-default submit">Submit</button>
      </form>
    </div>
  </div>
</template>

<script>
  import axios from 'axios'

  export default {
    name: 'CreateAvailability',

    data() {
      return {
        start: '',
        room: '',
        year: '',
        month: '',
        day: '',
        date: '',
        booking_type: '',
        newDate: '',
        message: '',
        doctor_id: this.$cookies.get('id'),
        response: ''
      }
    },

    watch: {
        date: function(query) {
            if (this.date != '' && this.start != ''){
                setTimeout(function() {
                    console.log(this);
                }, 500);

                this.getRooms();
            }
        },

        start: function(query) {
            if (this.date != '' && this.start != ''){
                setTimeout(function() {
                    console.log(this);
                }, 500);

                this.getRooms();
            }
        },
    },

    methods: {

      processForm: function () {
        this.newDate = this.date.split('-');
        axios.put('http://127.0.0.1:5000/availability', {
          start: this.start,
          room: this.room,
          year: this.newDate[0],
          month: this.newDate[1],
          day: this.newDate[2],
          booking_type: this.booking_type,
          doctor_id: this.doctor_id
        })
          .then(function (response) {
            alert(response.data.message);
          })
          .catch(error => {
            console.log(error)
            this.message = error.response.data.error.message;
          })
      },

      getRooms: function(event) {
        this.newDate = this.date.split('-');

        axios.get('http://127.0.0.1:5000/availability/room-availability', {
            params: {
                start: this.start,
                year: this.newDate[0],
                month: this.newDate[1],
                day: this.newDate[2],
            }
        }).then(response => {
                this.response = response.data.data
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
