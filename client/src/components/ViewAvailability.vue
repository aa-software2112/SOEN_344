/* eslint-disable */
<template>
  <div class="container reg-container" id="patient-reg">
    <table id="view">
      <th>Date</th>
      <th>Start</th>
      <th>Room</th>
      <th>Appointment Type</th>

      <tr class="container availability-item" v-for="(item) in results.data">
        <td> {{item['year']}}-{{item['month']}}-{{item['day']}}</td>
        <td> {{item['start']}}</td>
        <td> {{item['room']}}</td>
        <td> {{item['booking_type']}}</td>
      </tr>
    </table>
  </div>
</template>

<script>
  import axios from 'axios'

  export default {
    name: 'ViewAvailability',

    data() {
      return {
        doctor_id: this.$cookies.get('id'),
        results: ''
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
    }
  }

</script>
