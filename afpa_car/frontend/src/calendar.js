import Vue from 'vue/dist/vue.js';

// ~~~~~~~~ DEFAULT-TRIP ~~~~~~~~~~ //
new Vue({
    el: '#default_week',
    data: {
        update_default_week: false,
        preview_default_week : true,
        burger : true,
    },
    methods: {
        show_update: function () {
            this.update_default_week = true,
            this.preview_default_week = false,
            this.burger = false
        },
        hide_update: function () {
            this.update_default_week = false,
            this.preview_default_week = true,
            this.burger = true
        }
    }
});

// ~~~~~~~~ DATEPICKER ~~~~~~~~~~ //

import Calendar from './calendar/Calendar.vue';

new Vue({
    el: '#calendar_app',
    render: h => h(Calendar),
})

