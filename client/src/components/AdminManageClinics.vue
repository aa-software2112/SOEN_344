/* eslint-disable */
<template>
  <div class="container reg-container home">
    <div id="main-content-area" class="container-fluid ">
      <div class="contact-info">
        <div class=" clinic-info" value v-for="clinic in clinics" :value="clinic.id">
          <form v-on:submit.prevent>
            <h3> {{ clinic.name }} </h3>
            <div class="details">
              <h5>Details</h5>
              <p> Location: {{clinic.location }} </p>
              <p> Opens at: {{clinic.open_time}} </p>
              <p> Closes at: {{clinic.close_time}} </p>
              <p> Telephone: {{clinic.phone}} </p>
              <p> Rooms: {{clinic.nb_rooms}}</p>
              <div class="button-holder">
              <button v-b-modal="'modal' + clinic.id">Edit Details</button>
              </div>
              <!-- Modal Component -->
              <b-modal :id="'modal' + clinic.id" hide-footer centered title="Edit Clinic Details">
                <form id="form-availability" class="form" @submit.prevent="edit(clinic.id)">
                  <h3 class="error-message">{{message}}</h3>
                  <div class="form-group">
                    <label for="location">Location</label>
                    <input type="text" v-model="location">
                  </div>
                  <div class="form-group">
                    <label for="opening">Opening Time</label>
                    <input type="time" min="9:00" max="16:00" step="3600" v-model="opening">
                    <br>
                    <span class="help-text">Hours are 9am to 4pm</span>
                  </div>
                  <div class="form-group">
                    <label for="opening">Closing Time</label>
                    <input type="time" min="9:00" max="16:00" step="3600" v-model="closing">
                    <br>
                    <span class="help-text">Hours are 9am to 4pm</span>
                  </div>
                  <div class="form-group">
                    <label for="phone">Telephone</label>
                    <input type="tel" class="input" name="telephone" v-model="telephone">
                  </div>
                  <button type="submit" class="btn btn-default submit">Update</button>
                </form>
              </b-modal>
            </div>
            <div class="button-holder">
              <button v-on:click="showTableDoctors(clinic.id)">View Doctors</button>
              <button v-on:click="showTableNurses(clinic.id)">View Nurses</button>
              <button v-on:click="showTableAvailabilities(clinic.id)">View Availabilities</button>
            </div>
            <table id="view" class="show-table" v-if="displayDoctorTable & clinic.id == clinic_id">
              <th>Last Name</th>
              <th>First Name</th>
              <th>Specialty</th>
              <th>Physician Permit Number</th>
              <tr class="container patient-item" v-for="(item) in results_doctor.data">
                <td>{{item['last_name']}}</td>
                <td>{{item['first_name']}}</td>
                <td>{{item['specialty']}}</td>
                <td>{{item['physician_permit_nb']}}</td>
              </tr>
            </table>
            <table id="view" class="show-table" v-if="displayNurseTable & clinic.id == clinic_id">
              <th>Last Name</th>
              <th>First Name</th>
              <th>Access ID</th>
              <tr class="container patient-item" v-for="(item) in results_nurse.data">
                <td>{{item['last_name']}}</td>
                <td>{{item['first_name']}}</td>
                <td>{{item['access_id']}}</td>
              </tr>
            </table>
            <table id="view" class="show-table" v-if="displayAvailTable & clinic.id == clinic_id">
              <th>Doctor ID</th>
              <th>Start</th>
              <th>Room</th>
              <th>Date</th>
              <th>Booking Type</th>
              <tr class="container patient-item" v-for="(item) in results_availability.data">
                <td>{{item['doctor_id']}}</td>
                <td>{{item['start']}}</td>
                <td>{{item['room']}}</td>
                <td>{{item['day']}}/{{item['month']}}/{{item['year']}}</td>
                <td>{{item['booking_type']}}</td>
              </tr>
            </table>
          </form>
        </div>
        <form v-on:submit.prevent>
          <div class="button-holder">
            <button v-b-modal="'modal-newclinic'">Add Clinic</button>
          </div>
            <!-- Modal Component -->
              <b-modal :id="'modal-newclinic'" hide-footer centered title="Edit Clinic Details">
                <form id="form-availability" class="form" @submit.prevent="create()">
                  <h3 class="error-message">{{message}}</h3>
                  <div class="form-group">
                    <label for="name">Name</label>
                    <input type="text" v-model="name">
                  </div>
                  <div class="form-group">
                    <label for="location">Location</label>
                    <input type="text" v-model="location">
                  </div>
                  <div class="form-group">
                    <label for="opening">Opening Time</label>
                    <input type="time" min="9:00" max="16:00" step="3600" v-model="opening">
                    <br>
                    <span class="help-text">Hours are 9am to 4pm</span>
                  </div>
                  <div class="form-group">
                    <label for="opening">Closing Time</label>
                    <input type="time" min="9:00" max="16:00" step="3600" v-model="closing">
                    <br>
                    <span class="help-text">Hours are 9am to 4pm</span>
                  </div>
                  <div class="form-group">
                    <label for="phone">Telephone</label>
                    <input type="tel" class="input" name="telephone" v-model="telephone">
                  </div>
                  <button type="submit" class="btn btn-default submit">Create</button>
                </form>
              </b-modal>
        </form>

      </div>

    </div>

  </div>
</template>

<script>

  import axios from "axios";

  export default {
    name: 'Home',
    data() {
      return {
        msg: "Manage Clinics",
        loginMsgList: null,
        clinics: [],
        current_clinic: null,
        nurses: [],
        displayDoctorTable: false,
        displayNurseTable: false,
        displayAvailTable: false,
        results_doctor: '',
        results_nurse: '',
        results_availability: '',
        clinic_id: '',
      };
    },

    created() {
      this.getClinics();
      this.setCurrentClinic();
    },

    methods: {
      getLoginMessage() {
        const path = "http://127.0.0.1:5000/my-update";
        if (this.$cookies.get('logged') == 'True' && this.$cookies.get('user_type') == 'patient') {
          axios
            .get(path)
            .then(res => {
              this.loginMsgList = res.data.data;
              console.log(res)
            })
            .catch(error => {
              // eslint-disable-next-line
              console.error(error);
            });
        } else {
          console.log("no cookie")
        }
      },
      getClinics: function () {
        axios.get('http://127.0.0.1:5000/clinic', {}).then(response => {
          this.clinics = response.data.data
        })
          .catch(error => {
            console.log(error)
            this.message = error.response.data.error.message;
          })
      },
      getNurses: function () {
        axios.get('http://127.0.0.1:5000/nurse', {}).then(response => {
          this.nurses = response.data.data
        })
        .catch(error => {
          console.log(error)
          this.message = error.response.data.error.message;
        })
      },
      showTableDoctors: function (clinic_id) {
        this.clinic_id = clinic_id;
        this.displayNurseTable = false;
        this.displayAvailTable = false;
        if(this.displayDoctorTable){
          this.displayDoctorTable = false;
        } else {
          this.displayDoctorTable = true;
        }
        var self = this;
        self.submit = 'True';
        axios.get('http://127.0.0.1:5000/doctor', {
          params: {
            clinic_id: clinic_id
          }
        })
          .then(response => {
            self.results_doctor = response.data
          })
          .catch(function (error) {
            alert(error);
          });
      },
      showTableNurses: function (clinic_id) {
        this.clinic_id = clinic_id;
        this.displayDoctorTable = false;
        this.displayAvailTable = false;
        if(this.displayNurseTable){
          this.displayNurseTable = false;
        } else {
          this.displayNurseTable = true;
        }
        var self = this;
        self.submit = 'True';
        axios.get('http://127.0.0.1:5000/nurse', {
          params: {
            clinic_id: clinic_id
          }
        })
          .then(response => {
            self.results_nurse = response.data
          })
          .catch(function (error) {
            alert(error);
          });
      },
      showTableAvailabilities: function (clinic_id) {
        this.clinic_id = clinic_id;
        this.displayDoctorTable = false;
        this.displayNurseTable = false;
        if(this.displayAvailTable){
          this.displayAvailTable = false;
        } else {
          this.displayAvailTable = true;
        }
        var self = this;
        self.submit = 'True';
        axios.get('http://127.0.0.1:5000/availability', {
          params: {
            clinic_id: clinic_id
          }
        })
          .then(response => {
            self.results_availability = response.data
          })
          .catch(function (error) {
            alert(error);
          });
      },
      edit: function (clinic_id) {
        axios.put('http://127.0.0.1:5000/clinic', {
          clinic_id: clinic_id,
          location: this.location,
          open_time: this.opening,
          close_time: this.closing,
          phone: this.telephone,
        })
          .then(function (response) {
            location.reload();
            console.log(response.data.message);
          })
          .catch(error => {
            console.log(error)
            this.message = error.response.data.error.message;
          })
      },
      create: function() {
          axios.put('http://127.0.0.1:5000/clinic', {
          name: this.name,
          location: this.location,
          nb_rooms: 0,
          nb_doctors: 0,
          nb_nurses: 0,
          open_time: this.opening,
          close_time: this.closing,
          phone: this.telephone,
        })
          .then(function (response) {
            location.reload();
            console.log(response.data.message);
          })
          .catch(error => {
            console.log(error)
            this.message = error.response.data.error.message;
          })
      }
    },

    mounted() {
      console.log("in mounted");
      // hack to prevent double requests
      window.setTimeout(this.getLoginMessage, 1000);
    }
  };
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>
  .notifications {
    color: #000000;
    font-size: 20px;
    background-color: yellow;
  }
  .contact-info {
    margin-top: 0px;
  }
  form {
    max-width: 600px;
  }
  .button-holder {
    width: 550px;
    display: inline-flex;
    justify-content: space-evenly;
  }
  .details {
    font-family: "Playfair Display";
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    margin: 10px 0 15px 10px;
    font-size: 1rem;
    font-weight: 400;
    line-height: 1.5;
    background-color: rgb(0, 0, 0); /* Fallback color */
    background-color: rgba(0, 0, 0, 0.4); /* Black w/opacity/see-through */
    z-index: 2;
    border-radius: 5px;
    padding: 10px;
  }
  .details p {
    margin: 1px;
    font-family: "Playfair Display";
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
  }
  button {
    font-family: Arial;
  }

</style>
