/* eslint-disable */
<template>
  <div class="container reg-container home">
    <div id="main-content-area" class="container-fluid ">
      <h1>
        Welcome to UberSante
      </h1>
      <br>
      <h3>
        For a quick appointment with our doctors, this website provides an online medical appointment
        booking system that will greatly reduce your waiting time.
      </h3>

      <p class="notifications" v-for="loginMsg in loginMsgList">{{ loginMsg }}</p>
      <br>

      <div class="contact-info">
        <h2>Clinic Information:</h2>
        <div class=" clinic-info" value v-for="clinic in clinics" :value="clinic.id">
          <h3> {{ clinic.name }} </h3>
          <details>
            <p> Location: {{clinic.location }} </p>
            <p> Opens at: {{clinic.open_time}} </p>
            <p> Closes at: {{clinic.close_time}} </p>
            <p> Telephone: {{clinic.phone}} </p>
          </details>
        </div>

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
        msg: "Welcome to UberSante",
        loginMsgList: null,
        clinics: [],
        current_clinic: null,
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

</style>
