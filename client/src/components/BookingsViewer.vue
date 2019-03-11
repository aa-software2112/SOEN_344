/* eslint-disable */
<template>
    <div id="app-container">
    
        <!-- Modal Component -->
        <b-modal id="update-booking-modal" ref="updateCancelModal" centered title="Update Booking">
            <div class="">
                <label for="date">Select a new booking date</label>
                </br>
                <input type="Date" class="input" name="date" v-model="date" required>
                <b-button v-on:click="getAllSchedules" size="sm" variant="primary">Refresh</b-button>
            </div>
            <table id="view">
                <th>Time</th>
                <th>Doctor</th>
                <th>Room</th>
                <th>App. Type</th>
                <template v-for="(avail_dict, day_key) in schedules">
                    
                    <tr class="container" v-for="(avail, doctor_id) in avail_dict" :id="avail.id">
                     
                      <td> {{avail.start}} </td>
                      <td> {{getDoctor(avail) ? avail.doctor_name: avail.doctor_name}} </td>
                      <td> {{avail.room}} </td>
                      <td> {{avail.booking_type}} </td>
                     
                    </tr>
                </template>

            </table>
            
            
        </b-modal>
                
        <div id="main-content-area" class="main-color content-fluid">
            <div class="container reg-container">
                {{schedules}}
                <table id="view">
                    <th>Date(dd/mm/yyyy)</th>
                    <th>Time</th>
                    <th>Doctor</th>
                    <th>Room</th>
                    <th>App. Type</th>
                    <tr class="container" v-on:click="displayModal" v-for="(booking) in bookings" :id="'avail-'+booking['availability_id']">
                     
                      <td> {{booking.availability.day + '/' + booking.availability.month + '/' + booking.availability.year}}</td>
                      <td> {{booking.availability.start}} </td>
                      <td> {{booking.doctor_name}} </td>
                      <td> {{booking.availability.room}} </td>
                      <td> {{booking.availability.booking_type}} </td>
                     
                    </tr>

                </table>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
import Vue from 'vue';

export default {
    
    name: 'BookingsViewer',
    
    data() {
      return {
        bookings: '',
        avails: '',
        update_booking: '',
        schedules: '',
        date: '',
        result: '',
        message: ''
      }
    },

    methods: {

      submitForm(e) {
        e.preventDefault();
        return;
      },
      
      getBookings()
      {
        const p = 'http://127.0.0.1:5000/patient';

        axios.post(p,
          {
            patient_info: this.patient_info,
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
      
      getBookings()
      {
        const self = this;
        const p = 'http://127.0.0.1:5000/booking/' + this.$route.params.id;
        axios.get(p)
        .then(response => {
            self.bookings = response.data.data
            console.log(this.bookings)
            self.getAvailForBookings()
        })
        .catch(error => {
            self.bookings = null
        })
      
      },
      
      getAvailForBookings()
      {
        this.avails = {};
        const p = 'http://127.0.0.1:5000/availability'
        this.bookings.forEach((booking) => {
            axios.get(p, {
                params: {
                availability_id: booking.availability_id
                }
            })
            .then(response => {                
                Vue.set(booking, "availability",response.data.data)
                this.getDoctor(booking)
                
            })
        })
      },
      
      getDoctor(booking)
      {
        const d = 'http://127.0.0.1:5000/doctor';
        axios.get(d, {
            params: {
                id:booking.doctor_id
            }
        })
        .then(response => {
            Vue.set(booking, "doctor_name",response.data.data.first_name + " " + response.data.data.last_name)
        })
        .catch(error => {
            Vue.set(booking, "doctor_name","NO NAME FOUND")
        })
      
      },
      
      
      displayModal(e)
      {
        var booking_id = (e.target.parentElement.id).split("-")[1]
        this.bookings.forEach((booking) => {
            if(booking.id == booking_id)
            {
                this.update_booking = booking
                return false;
            }
        })
        this.$refs.updateCancelModal.show();
      },
    
    getAllSchedules()
    {
        const s = 'http://127.0.0.1:5000/schedule';
        console.log(this.date)
        if (this.date == "")
        {
            return
        }
        
        axios.post(s, 
        {
            date: this.date,
            request_type: "MONTHLY",
            appointment_request_type: "ALL"
        })
        .then(response => {
            this.schedules = response.data.data
            console.log(response.data)
            console.log(response.data.data)
        })
        .catch(error => {
            console.log(error)
        })
    }
    
    },
    
    created: function() {
        this.getBookings()
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>
</style>
