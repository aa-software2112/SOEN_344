/* eslint-disable */
<template>
  <div class="container reg-container" id="patient-reg">
    <h1> Search for an Appointment </h1>
    <form id="form-availability" @submit.prevent="processForm">
      <div class="form-group">
        <label for="request_type">Request Type</label>
        <select v-model="request_type" name="request_type" required>
          <option value="DAILY">Daily</option>
          <option value="MONTHLY">Monthly</option>
        </select>
      </div>
      <div class="form-group">
        <label for="appointment_request_type">Appointment Type</label>
        <select v-model="appointment_request_type" name="appointment_request_type" required>
          <option value="ANNUAL">Annual</option>
          <option value="WALKIN">Walkin</option>
        </select>
      </div>
      <div class="form-group">
        <label for="date">Year</label>
        <input type="Date" class="input" name="date" v-model="date" required>
      </div>
      <button type="submit" class="btn btn-default submit">Submit</button>
    </form>

    <div v-if="current_type === 'DAILY'">
      <div class="container availability-item" v-for="(item) in results.data">
        <p> Date: {{item['year']}}-{{item['month']}}-{{item['day']}} </p>
        <p> Room: {{item['room']}} </p>
        <p> Appointment Type: {{item['booking_type']}} </p>
        <p> Doctor: {{item['doctor_id']}} </p>
        <button :id="item['id']"> Book Appointment</button>
      </div>
    </div>
    <div v-else>
      <div v-for="(notUsed, index) in results.data">
        <div class="container availability-item" v-for="(item) in results.data[index]">
          <p> Date: {{item['year']}}-{{item['month']}}-{{item['day']}} </p>
          <p> Room: {{item['room']}} </p>
          <p> Appointment Type: {{item['booking_type']}} </p>
          <p> Doctor: {{item['doctor_id']}} </p>
          <button :id="item['id']"> Book Appointment</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'Schedule',
   data() {
    return {
       request_type: '',
      appointment_request_type: '',
      date: '',
      results: '',
      submit: '',
      current_type: ''
    };
  },
  methods: {
     processForm: function () {
       var self=this;
       self.submit='True';
      axios.post('http://127.0.0.1:5000/get_schedule',{request_type: this.request_type, appointment_request_type: this.appointment_request_type, date: this.date} )
        .then(response => {
            self.results = response.data
            self.current_type = this.request_type
          })
        .catch(function (error) {
          alert(error);
        });
    }
  }
}

</script>

<style>
 .availability-item{
        border-radius: 5px;
        text-align: left;
        background: rgba(0,0,0, 0.2);
        padding: 10px;
        margin: 10px auto 10px auto;
        max-width: 300px;
    }
  #list-results{
    margin: auto;
  }
</style>
