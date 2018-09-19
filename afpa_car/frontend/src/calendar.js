import Vue from 'vue/dist/vue.js';
import $ from 'jquery';

// ~~~~~~~~ DATEPICKER ~~~~~~~~~~ //

import Calendar from './components/Calendar.vue';

new Vue({
    el: '#calendar_app',
    render: h => h(Calendar),
})

// ~~~~~~~~ DEFAULT-TRIP ~~~~~~~~~~ //
new Vue({
    el: '#default_week',
    data: {
        update_default_week: false,
        preview_default_week: true, 
    },
    created: function () {
        
        for (var i = 0; i < 5; i++) {
            var element = document.getElementsByName('form-' + i + '-deactivate')[0]
            if (element.checked) {
                var divBgColor = document.getElementById('card-content-' + i)
                var mornDepTime = document.getElementsByName('form-' + i + '-morning_departure_time')[0]
                var mornArrTime = document.getElementsByName('form-' + i + '-morning_arriving_time')[0]
                var eveDepTime = document.getElementsByName('form-' + i + '-evening_departure_time')[0]
                var hasForStar = document.getElementsByName('form-' + i + '-has_for_start')[0]
                var userIsDriver = document.getElementsByName('form-' + i + '-user_is_driver')[0]

                mornDepTime.disabled = mornArrTime.disabled = eveDepTime.disabled = hasForStar.disabled = userIsDriver.disabled = element.checked

                divBgColor.style.backgroundColor = "#d4d8db"
            }
        }
    },

    methods: {
        show_update: function () {
            this.update_default_week = true
            this.preview_default_week = false
        },
        hide_update: function () {
            this.update_default_week = false
            this.preview_default_week = true
        },
        deactivate_fields: function (element_cliqued) {
            let i = element_cliqued.id.substr(8, 1)

            var divBgColor = document.getElementById('card-content-' + i)
            var mornDepTime = document.getElementsByName('form-' + i + '-morning_departure_time')[0]
            var mornArrTime = document.getElementsByName('form-' + i + '-morning_arriving_time')[0]
            var eveDepTime = document.getElementsByName('form-' + i + '-evening_departure_time')[0]
            var hasForStar = document.getElementsByName('form-' + i + '-has_for_start')[0]
            var userIsDriver = document.getElementsByName('form-' + i + '-user_is_driver')[0]
            
            mornDepTime.disabled = !mornDepTime.disabled
            mornArrTime.disabled = !mornArrTime.disabled
            eveDepTime.disabled = !eveDepTime.disabled
            hasForStar.disabled = !hasForStar.disabled
            userIsDriver.disabled = !userIsDriver.disabled
            
            divBgColor.style.backgroundColor = divBgColor.style.backgroundColor === ""  ? "#d4d8db" : ""

            
        },
        duplicate: function (i, initial_direction) {
            var direction = 1

            if( initial_direction === 0){
                direction = -1
            }

            var divBgColor1 = document.getElementById('card-content-' + i)       
            var mornDepTime1 = document.getElementsByName('form-' + i + '-morning_departure_time')[0]
            var mornArrTime1 = document.getElementsByName('form-' + i + '-morning_arriving_time')[0]
            var eveDepTime1 = document.getElementsByName('form-' + i + '-evening_departure_time')[0]
            var hasForStar1 = document.getElementsByName('form-' + i + '-has_for_start')[0]
            var userIsDriver1 = document.getElementsByName('form-' + i + '-user_is_driver')[0]
            var deactivate1 = document.getElementsByName('form-' + i + '-deactivate')[0]
            
            var divBgColor2 = document.getElementById('card-content-' + (i + direction))
            var mornDepTime2 = document.getElementsByName('form-' + ( i + direction ) + '-morning_departure_time')[0]
            var mornArrTime2 = document.getElementsByName('form-' + ( i + direction ) + '-morning_arriving_time')[0]
            var eveDepTime2 = document.getElementsByName('form-' + ( i + direction ) + '-evening_departure_time')[0]
            var hasForStar2 = document.getElementsByName('form-' + ( i + direction ) + '-has_for_start')[0]
            var userIsDriver2 = document.getElementsByName('form-' + ( i + direction ) + '-user_is_driver')[0]
            var deactivate2 = document.getElementsByName('form-' +( i + direction ) + '-deactivate')[0]
            
            mornDepTime2.value = mornDepTime1.value
            mornArrTime2.value = mornArrTime1.value
            eveDepTime2.value = eveDepTime1.value
            hasForStar2.value = hasForStar1.value
            userIsDriver2.checked = userIsDriver1.checked
            deactivate2.checked = deactivate1.checked

            mornDepTime2.disabled = mornDepTime1.disabled
            mornArrTime2.disabled = mornArrTime1.disabled
            eveDepTime2.disabled = eveDepTime1.disabled
            hasForStar2.disabled = hasForStar1.disabled
            userIsDriver2.disabled = userIsDriver1.disabled

            divBgColor2.style.backgroundColor = divBgColor1.style.backgroundColor
        }
    }
});


new Vue({
    delimiters: ['[[', ']]'],
    el: '#datepicker',
    components: {
        vuejsDatepicker,

    },
    data: {
        fr: {
            language: 'Français',
            months: ['Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre'],
            monthsAbbr: ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Juin', 'Juil', 'Août', 'Sep', 'Oct', 'Nov', 'Déc'],
            days: ['Dim', 'Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam'],
            yearSuffix: ''
        },
        message: '',
    },
    updated: function () {

        console.log("update")

    },
    methods: {
        customFormatter(date) {
            this.message = moment(date).format('D MMMM YYYY');
            console.log(this.message)
        }
    }
});











