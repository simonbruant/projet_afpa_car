// import Datepicker from '../../../../../../../_Program/npm install/node_modules/vuejs-datepicker'
// import {en, es} from '../../../../../../../_Program/npm install/node_modules/vuejs-datepicker/dist/locale'


// Desactivate inputs @Votre semaine type
var desactivate_fields = function (element_cliqued) {
    let i = element_cliqued.id.substr(8, 1)

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
}
// disable inputs @Votre semaine type
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
                var userIsDriver = document.getElementsByName('form-' + i + '-user_is_driver')[0]

                mornDepTime.disabled = element.checked
                mornArrTime.disabled = element.checked
                eveDepTime.disabled = element.checked
                hasForStar.disabled = element.checked
                userIsDriver.disabled = element.checked
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
        // dateSelected :function(e){
        //     console.log (e),
        //     this.message = e
        // },
        customFormatter(date) {
            this.message = moment(date).format('D MMMM YYYY');
            console.log(this.message)
        }
    }
});











