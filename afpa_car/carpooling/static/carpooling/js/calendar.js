// disable inputs @Votre semaine type
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

                mornDepTime.disabled = mornArrTime.disabled = eveDepTime.disabled = hasForStar.disabled =  element.checked

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
            
            mornDepTime.disabled = !mornDepTime.disabled
            mornArrTime.disabled = !mornArrTime.disabled
            eveDepTime.disabled = !eveDepTime.disabled
            hasForStar.disabled = !hasForStar.disabled
            
            divBgColor.style.backgroundColor = divBgColor.style.backgroundColor === ""  ? "#d4d8db" : ""

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











