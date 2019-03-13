/* eslint-disable */
<template>
  <div class="container reg-container" id="patient-reg">
    <div v-if="isLoggedNurse">
      <form id="form-availability" @submit.prevent="processFormPatientLookup">
        <h1> Search for a Patient </h1>
        <div class="form-group">
          <label for="patient_id">Patient Last Name</label>
          <input type="text" class="form-control" v-model="patient_name" id="patient_name">
          <button value="submit" type="submit" class="btn btn-default submit">Submit</button>
        </div>
      </form>

      <table id="view"> 
        <th>Health Card</th>
        <th>First Name</th>
        <th>Last Name</th>
        <th>Email</th>
        <th></th>
        <tr class="container patient-item" v-for="(item) in results_patient.data">
          <td>{{item['health_card_nb']}}</td>
          <td>{{item['first_name']}}</td>
          <td>{{item['last_name']}}</td>
          <td>{{item['email']}}</td>
          <td>
            <button :id="item['id']" v-on:click="storePatientId" @click="$event.target.classList.toggle('searchappt')"> Choose Patient</button>
          </td>
        </tr>
      </table>

      <form id="form-doctor" @submit.prevent="processFormDoctorLookup">
        <h1> Search for a Doctor (Optional) </h1>
        <div class="form-group">
          <label for="doctor_id">Doctor Last Name</label>
          <input type="text" class="form-control" v-model="doctor_name" id="doctor_name">
          <button value="submit" type="submit" class="btn btn-default submit">Submit</button>
        </div>
      </form>

      <table id="view"> 
        <th>Physician Permit</th>
        <th>First Name</th>
        <th>Last Name</th>
        <th>Specialty</th>
        <th></th>
        <tr class="container patient-item" v-for="(item) in results_doctor.data">
          <td>{{item['physician_permit_nb']}}</td>
          <td>{{item['first_name']}}</td>
          <td>{{item['last_name']}}</td>
          <td>{{item['specialty']}}</td>
          <td>
            <button :id="item['id']" v-on:click="storeDoctorId" @click="$event.target.classList.toggle('searchappt')"> Choose Doctor</button>
          </td>
        </tr>
      </table>
    </div>
    <form id="form-availability" @submit.prevent="processForm">
      <h1> Search for an Appointment </h1>
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
        <label for="date">Date</label>
        <input type="Date" class="input" name="date" v-model="date" required>
      </div>
      <button type="submit" class="btn btn-default submit">Submit</button>
    </form>

    <h3 class="success-message">{{success_message}}</h3>
    <h3 class="error-message">{{error_message}}</h3>

    <table id="view">
      <th v-if="doctor_id != 0">Doctor Name</th>
      <th>Date</th>
      <th>Start</th>
      <th>Room</th>
      <th>Appointment Type</th>
      <th>Book</th>

      <template v-if="current_type === 'DAILY'">
        <tr class="container availability-item" v-for="(item) in results.data" v-if="item['doctor_id'] == doctor_id || doctor_id == 0">
          <td v-if="doctor_id != 0">{{doctor_name}}</td>
          <td> {{item['year']}}-{{item['month']}}-{{item['day']}}</td>
          <td> {{item['start']}}</td>
          <td> {{item['room']}}</td>
          <td> {{item['booking_type']}}</td>
          <td v-if="!isLoggedNurse">
            <button :id="item['id']" v-on:click="addToCart($event)"> Add to cart </button>
          </td>
          <td v-else>
            <button :id="item['id']" v-on:click="addToCart($event)"> Create Appointment </button>
          </td>
        </tr>
      </template>

      <template v-else>
        <template v-for="(notUsed, index) in results.data">
          <template class="container availability-item" v-for="(item) in results.data[index]">
              <tr v-if="item['doctor_id'] == doctor_id || doctor_id == 0">
                <td v-if="doctor_id != 0">{{doctor_name}}</td>
                <td> {{item['year']}}-{{item['month']}}-{{item['day']}}</td>
                <td> {{item['start']}}</td>
                <td> {{item['room']}}</td>
                <td> {{item['booking_type']}}</td>
                <td v-if="!isLoggedNurse">
                  <button :id="item['id']" v-on:click="addToCart($event)"> Add to cart </button>
                </td>
                <td v-else>
                  <button :id="item['id']" v-on:click="addToCart($event)"> Create Appointment </button>
                </td>
              </tr>
          </template>
        </template>
      </template>

    </table>
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
        results_patient: '',
        results_doctor: '',
        submit: '',
        current_type: '',
        patient_name: '',
        patient_id:'',
        doctor_id:'',
        doctor_name:'',
        availability_id: '',
        success_message: '',
        error_message: ''
      };
    },
    methods: {
      processForm: function () {
        var self = this;
        self.submit = 'True';
        if (this.$cookies.get('user_type') == 'nurse'){
          try {
            self.patient_id = patient_id
          } catch (e){
              this.error_message = "Please choose a patient"
              return
          }
        }
        try {
          var useable_doctor_id = doctor_id
        } catch (e) {
          var useable_doctor_id = 0
        }
        axios.post('http://127.0.0.1:5000/schedule', {
        request_type: this.request_type,
        appointment_request_type: this.appointment_request_type,
        date: this.date
        })
          .then(response => {
            self.results = response.data
            self.current_type = this.request_type
            self.doctor_id = useable_doctor_id
          })
          .catch(function (error) {
            alert(error);
          });
      },
      processFormPatientLookup: function () {
        var self = this;
        self.submit = 'True';
        axios.get('http://127.0.0.1:5000/patient', {
            params: {
              last_name: this.patient_name
            }
        })
          .then(response => {
            self.results_patient = response.data
          })
          .catch(function (error) {
            alert(error);
          });
      },
      processFormDoctorLookup: function () {
        var self = this;
        self.submit = 'True';
        axios.get('http://127.0.0.1:5000/doctor', {
            params: {
              last_name: this.doctor_name
            }
        })
          .then(response => {
            self.results_doctor = response.data
          })
          .catch(function (error) {
            alert(error);
          });
      },
      storePatientId: function (e) {
        if (self.doctor_id == e.currentTarget.getAttribute('id')){
          self.patient_id = 0
        } else {
          self.patient_id = e.currentTarget.getAttribute('id')
        }
      },
      storeDoctorId: function (e) {
        if (self.doctor_id == e.currentTarget.getAttribute('id')){
          self.doctor_id = 0
        } else {
          self.doctor_id = e.currentTarget.getAttribute('id')
        }
      },
      addToCart: function(event) {

      if (this.$cookies.get('user_type') != 'patient' && this.$cookies.get('user_type') != 'nurse' ) {
      this.error_message = "Must be a patient or a nurse to book"
      return
      }

      this.availability_id = event.currentTarget.id.toString();
      console.log(this.availability_id);

      if (this.$cookies.get('user_type') == 'patient'){
        self.patient_id = this.$cookies.get('id')
        if (this.appointment_request_type == "ANNUAL") {
          var p = 'http://127.0.0.1:5000/annual-appointment';
        } else {
          var p = 'http://127.0.0.1:5000/walkin-appointment'
        }
      } else if(this.$cookies.get('user_type') == 'nurse') {
        if (this.appointment_request_type == "ANNUAL") {
          var p = 'http://127.0.0.1:5000/annual-appointment-nurse';
        } else {
          var p = 'http://127.0.0.1:5000/walkin-appointment-nurse'
        }
      };


        axios.put(p, {
          availability_id: this.availability_id,
          patient_id: self.patient_id
        }).then(response => {
        this.success_message = 'Successfully added appointment to cart';
        this.error_message = '';
        console.log(response);
        })
        .catch(error => {
        console.log(error)
        this.error_message = error.response.data.error.message;
        this.success_message = '';
        })
      }
      
    },
    computed:{  
      isLoggedNurse: function()
        {
            return this.$cookies.get('logged') == 'True' && this.$cookies.get('user_type') == 'nurse'
        }
    }
  }

</script>
