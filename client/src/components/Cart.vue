<template>
  <div id="app-container">
    <div id="main-content-area">
      <h1>My Cart</h1>
      <div class="container reg-container" id="my-appointments">
        <ul>
          <li v-for="appointment in appointment_list">
            {{appointment}} <button>checkout</button>
          </li>
        </ul>
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

  created () {
    this.log();
    axios
      .get('http://localhost:5000/cart')
      .then(res => {
        this.appointment_list = res.data.appointments;
        console.log(res);

      });

  }


}

</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>

</style>
