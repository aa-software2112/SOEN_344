/* eslint-disable */
<template>
    <div id="app-container"> 
          <div id="main-content-area" class="main-color content-fluid">   
         <h1> Available appointments: </h1>
        <AvailabilityItem></AvailabilityItem>
            </div>    
    </div>    
</template>

<script>
import axios from 'axios'
import AvailabilityItem from './AvailabilityItem';

export default {
  name: 'Schedule',
  components: {
    'AvailabilityItem': AvailabilityItem
  },
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

</style>