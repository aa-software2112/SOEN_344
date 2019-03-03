<template>
  <div id="app-container">
    <div id="main-content-area">
      <h1 id="checkout" align="left">Checkout</h1>
      <div class="container reg-container" id="my-appointments">
        <div id="appointment" v-for="appointment in appointment_list">
          {{"type: " + appointment.availability.booking_type }}
          {{appointment.availability.day + "/" + appointment.availability.month + "/" + appointment.availability.year}}
          {{"start time:" + appointment.availability.start}}
          <button @click="remove_from_cart(appointment.availability.id)">remove</button>
          <button @click="checkout(appointment.availability.id)">checkout</button>
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
        patient_id: null
      };
    },

    methods: {
      log: function () {
        console.log("Hello world");
        console.log(this);
      },
      
      remove_from_cart: function(availability_id) {
        console.log("removing " + availability_id + " from cart");
        const url = "http://localhost:5000/appointment";
        console.log(url);
        axios.delete(url, {
          params: {
            patient_id: this.patient_id,
            availability_id:  availability_id
          }
        })
          .then(response => {
            console.log(response);
          });
      },

      checkout: function (availability_id) {
        alert("in checkout fct");
        const url = "http://localhost:5000/booking";
        console.log(url);
        axios.put(url, {
          params: {
            patient_id: this.patient_id,
            availability_id:  availability_id
          }
        })
        .then(response => {
            console.log(response);
          });

      }


    },

    created() {
      this.log();
      axios
        .get('http://localhost:5000/cart')
        .then(res => {
          console.log(res);
          this.appointment_list = res.data.data.appointment_list;
          this.patient_id = res.data.data.patient_id;
          console.log("the appointment list");
          console.log(this.appointment_list);
          console.log("the patient_id");
          console.log(this.patient_id);
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
