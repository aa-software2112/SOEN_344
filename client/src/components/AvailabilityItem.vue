/* eslint-disable */
<template>
    <div class="container availability-item" id="availability-item">                
           <p> Doctor: {{doctor_name}}  </p>
           <p> Appointment Type: {{appointment_type}} </p>
           <p> Room: {{room}} </p>
            <p> Year: {{year}} Month: {{month}}  Day: {{day}} </p>
            <button :id="availability_id"> Book Appointment </button>
    </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'AvailabilityItem',

  data() {
    return {
        doctor_name: null,
        room: null,
        year: null,
        month: null,
        day: null,
        availability_id: null,
        appointment_type: null
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>
    .availability-item{
        border-radius: 5px;
        text-align: left;
        background: rgba(255,255,255, 0.5);
        padding: 10px;
    }
</style>