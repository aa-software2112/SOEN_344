<template>
  <div class="container reg-container" id="patient-reg">

    <h1> My Cart </h1>
    <table id="view">
      <th>Type</th>
      <th>Day</th>
      <th>Month</th>
      <th>Year</th>
      <th>Actions</th>

      <template>
        <tr class="container availability-item" v-for="appointment in appointment_list">
          <td> {{appointment.availability.booking_type}}</td>
          <td> {{appointment.availability.day}} </td>
          <td> {{appointment.availability.month}} </td>
          <td> {{appointment.availability.year}}</td>
          <td>
           <button @click="remove_from_cart(appointment.availability.id)">remove</button>
            <button @click="checkout(appointment.availability.id)">checkout</button>
          </td>

        </tr>
      </template>

    </table>
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
        const this_page = "http://127.0.0.1:5000/cart";
        const backend_url = "http://127.0.0.1:5000/appointment";
        console.log("sending delete request to " + backend_url);
        axios.delete(backend_url, {
          params: {
            patient_id: this.patient_id,
            availability_id:  availability_id
          }
        })
          .then(response => {
            // if no error is thrown
            console.log(response);
            // refresh page to show changes
            axios.get(this_page);
          })
          .catch(error =>
          console.log("An error occurred: " + error));
      },

      checkout: function (availability_id) {
        console.log("checking out " + availability_id + " from cart");
        const this_page = "http://127.0.0.1:5000/cart";
        const url = "http://127.0.0.1:5000/booking";
        console.log("sending put request to " + url);
        axios.put(url, {
          params: {
            patient_id: this.patient_id,
            availability_id:  availability_id
          }
        })
        .then(response => {
            // if no error is thrown
            console.log(response);
            // refresh the page to show cart update
            axios.get(this_page);
          })
          .catch(error => {
            console.log("An error occurred: " + error)
          });

      }


    },

    created() {
      console.log("in created(), from Cart.vue");
      axios
        .get('http://127.0.0.1:5000/cart')
        .then(res => {
          console.log(res);
          this.appointment_list = res.data.data.appointment_list;
          this.patient_id = res.data.data.patient_id;
          console.log("the appointment list");
          console.log(this.appointment_list);
          console.log("the patient_id");
          console.log(this.patient_id);
        })
        .catch(error => {
          console.log("On created(), couldn't GET http://127.0.0.1:5000/cart " + error)
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

  table, th, td {
    border: 1px solid black;
  }

</style>
