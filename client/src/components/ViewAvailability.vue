/* eslint-disable */
<template>
  <div id="app">
    <div class="container reg-container" id="patient-reg">
      <h1> View, Edit and Cancel Availabilities</h1>
      <table id="view">
        <th>Date</th>
        <th>Start</th>
        <th>Room</th>
        <th>Appointment Type</th>
        <th>Edit</th>
        <th>Cancel</th>

        <tr class="container availability-item" v-for="(item) in results.data">

          <td> {{item['year']}}-{{item['month']}}-{{item['day']}}</td>
          <td> {{item['start']}}</td>
          <td> {{item['room']}}</td>
          <td> {{item['booking_type']}}</td>
          <td>
            <button v-b-modal="'modal' + item['id']">Edit</button>
          </td>
          <td>
            <button :id="item['id']" v-on:click="cancel(item['id'])"> Cancel</button>
          </td>

          <!-- Modal Component -->
          <b-modal :id="'modal' + item['id']" hide-footer centered title="Edit Availability">
            <form id="form-availability" class="form" @submit.prevent="edit(item['id'])">
              <h3 class="error-message">{{message}}</h3>
              <div class="form-group">
                <label for="start">Appointment Time</label>
                <input v-if="item['booking_type'] === 'WALKIN'" type="time" min="9:00" max="16:00" step="1200"
                       v-model="start">
                <input v-else type="time" min="9:00" max="16:00" step="3600" v-model="start">
                <br>
                <span class="help-text">Hours are 9am to 4pm</span>
              </div>
              <div class="form-group">
                <label for="room">Room</label>
                <select v-model="room" name="book_type">
                  <option value="101">101</option>
                  <option value="102">102</option>
                  <option value="103">103</option>
                  <option value="104">104</option>
                  <option value="105">105</option>
                </select>
              </div>
              <div class="form-group">
                <label for="date">Date</label>
                <input type="Date" class="input" name="date" v-model="date">
              </div>
              <button type="submit" class="btn btn-default submit">Update</button>
            </form>
          </b-modal>

        </tr>

      </table>
    </div>
  </div>
</template>

<script>
  import axios from 'axios'

  export default {
    name: 'ViewAvailability',

    data() {
      return {
        doctor_id: this.$cookies.get('id'),
        results: '',
        id: '',
        start: '',
        room: '',
        year: '',
        month: '',
        day: '',
        date: '',
        booking_type: '',
        newDate: '',
        message: '',
      };
    },

    created: function () {
      var self = this;

      axios.put('http://127.0.0.1:5000/viewavailability', {
        doctor_id: self.doctor_id
      })
        .then(response => {
          self.results = response.data
          console.log(response)
        })
        .catch(error => {
          console.log(error)
        })
    },

    methods: {
      edit: function (identifer) {
        this.newDate = this.date.split('-');
        axios.put('http://127.0.0.1:5000/availability/' + identifer, {
          start: this.start,
          room: this.room,
          year: this.newDate[0],
          month: this.newDate[1],
          day: this.newDate[2],
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

      cancel: function (identifier) {
        this.id = identifier;
        axios.delete('http://127.0.0.1:5000/availability', {
          data: {id: this.id}
        })
          .then(response => {
            location.reload();
          })
          .catch(error => {
            console.log(error)
          })
      }
    }
  }

</script>
