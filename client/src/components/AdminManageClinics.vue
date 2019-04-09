/* eslint-disable */
<template>
  <div class="container reg-container home">
    <div id="main-content-area" class="container-fluid ">
      <div class="contact-info">
        <div class=" clinic-info" value v-for="clinic in clinics" :value="clinic.id">
          <form v-on:submit.prevent>
            <h3> {{ clinic.name }} </h3>
            <div>
              <p> Location: {{clinic.location }} </p>
              <p> Opens at: {{clinic.open_time}} </p>
              <p> Closes at: {{clinic.close_time}} </p>
              <p> Telephone: {{clinic.phone}} </p>
            </div>
            <div class="button-holder">
              <button v-on:click="showTableDoctors(clinic.id)">View Doctors</button>
              <button v-on:click="showTableNurses">View Nurses</button>
              <button v-on:click="showTableAvailabilities">View Availabilities</button>
            </div>
            <table class="show-table" v-if="displayDoctortable">
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
          </form>
          <div class="display-table" v-if="displayNurseTable">
            <tr></tr>
            <tr></tr>
          </div>
          <div class="display-table" v-if="displayAvailTable">
            <tr></tr>
            <tr></tr>
          </div>
        </div>
        <form>
          <div class="button-holder">
            <button>Add Clinic</button>
          </div>
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
        displayDoctortable: false,
        displayNurseTable: false,
        displayAvailTable: false,
        results_doctor: '',
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
        if(this.displayDoctortable){
          this.displayDoctortable = false;
          console.log(this.displayDoctortable)
        } else {
          this.displayDoctortable = true;
          console.log(this.displayDoctortable)
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
      showTableNurses: function () {

      },
      showTableAvailabilities: function () {

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


</style>
