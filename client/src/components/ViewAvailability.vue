/* eslint-disable */
<template>
  <div id="app">
    <div class="main-color">
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
            <button :id="item['id']" v-on:click="edit(item['id'])"> edit</button>
          </td>
          <td>
            <button :id="item['id']" v-on:click="cancel(item['id'])"> Cancel</button>
          </td>

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
        id: ''
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
      edit: function (identifier) {
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
