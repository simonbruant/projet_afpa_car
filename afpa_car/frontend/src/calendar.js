import Vue from 'vue/dist/vue.js';
import $ from 'jquery';



// ~~~~~~~~ DATEPICKER ~~~~~~~~~~ //

import Calendar from './calendar/Calendar.vue';

new Vue({
    el: '#calendar_app',
    render: h => h(Calendar),
})


// ~~~~~~~~ DEFAULT-TRIP ~~~~~~~~~~ //
new Vue({
    el: '#default_week',
    data: {
        update_default_week: false,
        preview_default_week: true
    },
    created: function () {
        for (var i = 0; i < 5; i++) {
            var element = document.getElementsByName('form-' + i + '-deactivate')[0]

            if (element.checked) {
                var mornDepTime = document.getElementsByName('form-' + i + '-morning_departure_time')[0]
                var mornArrTime = document.getElementsByName('form-' + i + '-morning_arriving_time')[0]
                var eveDepTime = document.getElementsByName('form-' + i + '-evening_departure_time')[0]
                var hasForStar = document.getElementsByName('form-' + i + '-has_for_start')[0]

                mornDepTime.disabled = element.checked
                mornArrTime.disabled = element.checked
                eveDepTime.disabled = element.checked
                hasForStar.disabled = element.checked
            }
        }
    },

    methods: {
        show_update: function () {
            this.update_default_week = true
            this.preview_default_week = false
            console.log("script lancé")
        },
        hide_update: function () {
            this.update_default_week = false
            this.preview_default_week = true
        },
        deactivate_fields: (element_cliqued) => {

            console.log("eeeeeeeeeeeeeeeee")
            console.log(element_cliqued)
            let i = element_cliqued.id.substr(8, 1)
            
            var mornDepTime = document.getElementsByName('form-' + i + '-morning_departure_time')[0]
            var mornArrTime = document.getElementsByName('form-' + i + '-morning_arriving_time')[0]
            var eveDepTime = document.getElementsByName('form-' + i + '-evening_departure_time')[0]
            var hasForStar = document.getElementsByName('form-' + i + '-has_for_start')[0]
            
            mornDepTime.disabled = !mornDepTime.disabled
            mornArrTime.disabled = !mornArrTime.disabled
            eveDepTime.disabled = !eveDepTime.disabled
            hasForStar.disabled = !hasForStar.disabled

        }
        // disable_fields: function (element_cliqued) {
        //     let i = element_cliqued.id.substr(8, 1)

        //     var mornDepTime = document.getElementsByName('form-' + i + '-morning_departure_time')[0]
        //     var mornDepTime = document.getElementsByName('form-' + i + '-morning_departure_time')[0]
        //     var mornArrTime = document.getElementsByName('form-' + i + '-morning_arriving_time')[0]
        //     var eveDepTime = document.getElementsByName('form-' + i + '-evening_departure_time')[0]
        //     var hasForStar = document.getElementsByName('form-' + i + '-has_for_start')[0]

        //     mornDepTime.disabled = !mornDepTime.disabled
        //     mornArrTime.disabled = !mornArrTime.disabled
        //     eveDepTime.disabled = !eveDepTime.disabled
        //     hasForStar.disabled = !hasForStar.disabled
        // }
    }
});
