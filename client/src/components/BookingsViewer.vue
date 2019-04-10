/* eslint-disable */
<template>
    <div id="app-container">
    
        <!-- Modal Component -->
        <b-modal id="update-booking-modal" ref="updateCancelModal" centered title="Update Booking">
            <div v-if="!is_for_doctor" class="refresh-div">
                <label for="date">Select a new booking date</label>
                </br>
                <input type="Date" class="input" name="date" v-model="date" required>
                <b-button v-on:click="getAllSchedules" size="sm" variant="primary">Refresh</b-button>
            </div>
            
            <div v-if="update_booking != ''" class="container">
                <div class="update-avail-title container justify-content-start"> 
                    <div class="row">
                        Selected Booking... 
                    </div>
                </div>
                <div class="container update-avail-container justify-content-start"> 
                    <p class="row update-avail-p">Start Time: {{update_booking.availability.start}}</p>
                    <p class="row update-avail-p">Doctor Name: {{update_booking.doctor_name}}</p>
                    <p class="row update-avail-p">Room: {{update_booking.availability.room}}</p>
                    <p class="row update-avail-p">Booking Type: {{update_booking.availability.booking_type}}</p>
                </div>
            </div>
            
            <div v-if="schedules != ''"id="update-schedule-container" class="container justify-content-center">
                <table class="table-view" id="mini-sched-table">
                    <th>Date</th>
                    <th>Time</th>
                    <th>Doctor</th>
                    <th>Room</th>
                    <th>App. Type</th>
                    <template v-for="(avail_dict, day_key) in schedules">
                        
                        <tr v-on:click="selectForUpdating" v-if="avail.free == 1" class="container" v-for="(avail, doctor_id) in avail_dict" :id="avail.id">
                          <td> {{avail.year + "/" + avail.month + "/" + avail.day}} </td>
                          <td> {{avail.start}} </td>
                          <td> {{getDoctor(avail) ? avail.doctor_name: avail.doctor_name}} </td>
                          <td> {{avail.room}} </td>
                          <td> {{avail.booking_type}} </td>
                         
                        </tr>
                    </template>

                </table>
            </div>
            
            <div class="container" v-if="update_to_availability.start != null" >
                <div class="update-avail-title container justify-content-start"> 
                    <div class="row">
                        Update to... 
                    </div>
                </div>
                <div class="container update-avail-container justify-content-start">
                    <p class="row update-avail-p">Start Time: {{update_to_availability.start}}</p>
                    <p class="row update-avail-p">Doctor Name: {{update_to_availability.doctor_name}}</p>
                    <p class="row update-avail-p">Room: {{update_to_availability.room}}</p>
                    <p class="row update-avail-p">Booking Type: {{update_to_availability.booking_type}}</p>
                </div>
            </div>
            <div slot="modal-footer" class="w-100">
                <b-button size="sm" class="float-right mbutton" variant="secondary" @click="show=false">Close</b-button>
                <b-button size="sm" class="float-right mbutton" variant="danger" @click="cancelBooking">Cancel Selected Booking</b-button>
                <b-button v-if="!is_for_doctor" size="sm" class="float-right mbutton" variant="primary" @click="updateBooking">Update Booking</b-button>
            </div>
            
        </b-modal>
                
        <div id="main-content-area" class="main-color content-fluid">
            <div class="container reg-container">
                <h1>Bookings</h1>
                </br>
                <table id="view">
                    <th>Date <span class="hint">(DD/MM/YYYY)</span></th>
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
        update_to_availability: Object(),
        schedules: '',
        date: '',
        result: '',
        message: '',
        is_for_doctor: '',
        update_cancel_message: ''
      }
    },

    methods: {

      submitForm(e) {
        e.preventDefault();
        return;
      },
      
      
      getBookings()
      {
        const self = this;        
        var p ="";
        if(this.$route.path.includes("doctor"))
        {
            p = 'http://127.0.0.1:5000/booking/doctor/' + this.$route.params.id;
            this.is_for_doctor = true;
        }
        else if(this.$route.path.includes("bookingsViewer/"))
        {
            p = 'http://127.0.0.1:5000/booking/' + this.$route.params.id;
        }
        else
        {
            p = 'http://127.0.0.1:5000/booking/' + this.$cookies.get('id');
        }
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
            console.log(booking)
            if(booking.availability_id == booking_id)
            {
                this.update_booking = booking
                return false;
            }
        })
        console.log(this.update_booking)
        this.date = ""
        this.update_to_availability = Object()
        this.schedules = ""
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
            appointment_request_type: "ALL",
            patient_id: this.$cookies.get('id')
        })
        .then(response => {
            this.schedules = response.data.data
            console.log(response.data)
            console.log(response.data.data)
        })
        .catch(error => {
            console.log(error)
        })
    },
    
    selectForUpdating(e)
    {
        var children = e.target.parentElement.children
        Vue.set(this.update_to_availability, "start", children[1].innerText)
        Vue.set(this.update_to_availability, "doctor_name", children[2].innerText)
        Vue.set(this.update_to_availability, "room", children[3].innerText)
        Vue.set(this.update_to_availability, "booking_type", children[4].innerText)
        Vue.set(this.update_to_availability, "availability_id", e.target.parentElement.id)
    
    },
    
    updateBooking() {
        
        const u = 'http://127.0.0.1:5000/booking'
        axios.put(u,
        {
            availability_id:this.update_to_availability.availability_id,
            booking_id:this.update_booking.id,
            patient_id:this.update_booking.patient_id
        })
        .then(response => {
            console.log(response)
            location.reload();
        })
        .catch(error => {
            console.log(error)
        })
    
    },
    
    cancelBooking() {
        
        const u = 'http://127.0.0.1:5000/booking'
        axios.delete(u,
        {
            params: {booking_id:this.update_booking.id}
        })
        .then(response => {
            console.log(response)   
            location.reload();
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
