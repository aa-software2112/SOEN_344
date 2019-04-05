/* eslint-disable */
<template>

  <div id="app-container">
    <div id="main-content-area" class="main-color content-fluid">
      <div>
        <PatientSearch></PatientSearch>
        <DoctorSearch></DoctorSearch>
      </div>
    </div>
  </div>

</template>

<script>
  import axios from 'axios';
  import PatientSearch from './PatientSearch';
  import DoctorSearch from './DoctorSearch';

  export default {

    components: {
      PatientSearch,
      DoctorSearch
    },

    name: 'NurseViewBooking',

    data() {
      return {
        patient_info: '',
        result: '',
        message: ''
      }
    },

    methods: {

      submitForm(e) {
        e.preventDefault();
        this.getPatientId();
        return;
      },

      getPatientId() {
        const p = 'http://127.0.0.1:5000/patient';

        axios.get(p,
          {
            params: {patient_info: this.patient_info}
          })
          .then(response => {
            this.message = response.data.message;
            if (!Array.isArray(response.data.data)) {
              response.data.data = [response.data.data]
              console.log(response)
            }
            this.result = response.data
            console.log(response.data.data);
          })
          .catch(error => {
            console.log(error)
            this.message = error.response.data.error.message;
          })
      },

      redirect(e) {
        const link = e.target.parentElement.getAttribute("data-href")
        console.log(e)
        console.log(e.target.parentElement.getAttribute("data-href"))
        this.$router.push({path: link})

      }
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>
</style>
