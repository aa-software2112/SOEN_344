<template>
  <div id="app-container">
    <div id="main-content-area">
      <h1 id="checkout" align="left">Checkout</h1>
      <div class="container reg-container" id="my-appointments">
        <div id="appointment" v-for="appointment in appointment_list">
          {{"type: " + appointment.availability.booking_type }}
          {{appointment.availability.day + "/" + appointment.availability.month + "/" + appointment.availability.year}}
          {{"start time:" + appointment.availability.start}}
          <button>checkout</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  import axios from 'axios'

  export default {
    name: 'Cart',


    data() {
      return {
        appointment_list: [],
      };
    },

    methods: {
      log: function () {
        console.log("Hello world");
        console.log(this);
      }


    },

    created() {
      this.log();
      axios
        .get('http://localhost:5000/cart')
        .then(res => {
          this.appointment_list = res.data.data;
          console.log(res);

        });

    }


  }

</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>
  #checkout {
    margin-left: 20px;
  }

  #appointment {
    margin-bottom: 10px;
  }
</style>
