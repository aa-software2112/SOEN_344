/* eslint-disable */
<template>
    
    <div class="container reg-container">
        <form @submit="submitForm" class="reg-form" action="">
            <h1>View Doctor Bookings</h1>
            <h3 class="error-message">{{message}}</h3>
            </br>
            <div class="form-group">
              <label for="doctor_info">Doctor (Last Name)</label>
              <input type="text" class="form-control" v-model="doctor_info" id="doctor_info">
            </div>
            <button value="submit" type="submit" class="btn btn-default submit">Submit</button>
        </form>
        </br>
        <table v-if="result.data" id="view">
            <th>First Name</th>
            <th>Last Name</th>
            <th>Physician Patient Nb.</th>
            
                <tr class="container" v-on:click="redirect" v-for="(item) in result.data" :data-href="'/bookingsViewer/doctor/'+item['id']">
                 
                  <td> {{item['first_name']}}</td>
                  <td> {{item['last_name']}}</td>
                  <td> {{item['physician_permit_nb']}}</td>
                  
                </tr>

        </table>
    </div>
</template>

<script>
import axios from 'axios';

export default {
    
    name: 'DoctorSearch',
    
    data() {
      return {
        doctor_info: '',
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
      
      getPatientId()
      {
        const p = 'http://127.0.0.1:5000/doctor';

        axios.get(p,
          {
            params: {last_name: this.doctor_info}
          })
          .then(response => {
            this.message = response.data.message;
            if (!Array.isArray(response.data.data))
            {
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
      
      redirect(e)
      {
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
