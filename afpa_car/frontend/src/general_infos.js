import Vue from 'vue/dist/vue.js';

/* ###### Vue.Js pour l'affichage du radio "Posedez-vous une voiture" dans infos generales ###### */

new Vue({
    el: '#view_car_owner',
    data: {
        isVisible: false,
        isVisibleCar : false,
        isVisibleLicense : false
    },
    mounted: function() { 
        if ( id_driver_license_0.checked ){
            this.isVisible = true
        }  
        },
    methods: {
        show: function () {
            this.isVisible = true
        },
        hide: function () {
            this.isVisible = false
        },
        show_error_message_car: function() {
            this.isVisibleCar = true
        },
        show_error_message_license: function() {
            this.isVisibleLicense = true
        }
    }
});