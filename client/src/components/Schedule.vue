/* eslint-disable */
<template>
  <div class="container reg-container" id="patient-reg">

    <form id="form-availability" @submit.prevent="processForm">
      <div class="form-group">
      <label for="request_type">Request Type</label>
      <select v-model="request_type" name="request_type">
        <option value="DAILY">Daily</option>
        <option value="MONTHLY">Monthly</option>
       </select>
      </div>
      <div class="form-group">
      <label for="appointment_request_type">Appointment Type</label>
      <select v-model="appointment_request_type" name="appointment_request_type">
        <option value="ANNUAL">Annual</option>
        <option value="WALKIN">Walkin</option>
      </select>
      </div>
      <div class="form-group">
        <label for="date">Year</label>
        <input type="Date" class="input" name="date" v-model="date">
      </div>
      <button type="submit" class="btn btn-default submit">Submit</button>
      </form>

       <div id="results">
         <ul id="example-1">
             <div v-for="(notUsed, index) in results.data">
               <div v-for="(item) in results.data[index]">
                   <div class="container availability-item" id="availability-item">
                      <p> Doctor: {{item['doctor_id']}}  </p>
                      <p> Appointment Type: {{item['booking_type']}} </p>
                      <p> Room: {{item['room']}} </p>
                      <p> {{item['year']}}-{{item['month']}}-{{item['day']}} </p>
                      <button :id="availability_id"> Book Appointment </button>
                  </div>
              </div>
             </div>
         </ul>
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
      results: ''
    };
  },
  methods: {
     processForm: function () {
       var self=this;
      axios.post('http://127.0.0.1:5000/get_schedule',{request_type: this.request_type, appointment_request_type: this.appointment_request_type, date: this.date} )
        .then(response => {
            self.results = response.data
            alert(self.results)
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
        background: rgba(255,255,255, 0.5);
        padding: 10px;
        margin: 10px;
    }
</style>
