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

const app = new Vue({
    el: '#datepicker',
    components: {
        vuejsDatepicker
    },
    data: { fr: { 
        language: 'Français',
        months: ['Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre'], 
        monthsAbbr: ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Juin', 'Juil', 'Août', 'Sep', 'Oct', 'Nov', 'Déc'], 
        days: ['Dim', 'Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam'],
        yearSuffix: '' } }
    });
    

