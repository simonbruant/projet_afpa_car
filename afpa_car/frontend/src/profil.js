import Vue from 'vue/dist/vue.js';
import $ from 'jquery';

/* ###### Fonction d'affichage pour la side-bar ###### */

// $(document).ready(function () {
//     $("#filtre_url_contenu a").each(function (index) {
//         if (this.href == document.location.href) {
//             $(this).addClass('active')
//             console.log("ok jquery")
//         }
//         /* adresses */
//         else if (this.href == document.location.href.substr(0, 40)) {
//             $(this).addClass('active')
//         }
//         /* vehicule */
//         else if (this.href == document.location.href.substr(0, 41)) {
//             $(this).addClass('active')
//         }
//     })
// });

new Vue({
    el: '#app_filtre_url_contenu',
    data: {

    },
    created: function() { 
        $("#filtre_url_contenu a").each(function (index) {
            if (this.href == document.location.href) {
                $(this).addClass('active')
                console.log("ok vuejs")
            }
            /* adresses */
            else if (this.href == document.location.href.substr(0, 37)) {
                $(this).addClass('active')
            }
            /* vehicule */
            else if (this.href == document.location.href.substr(0, 38)) {
                $(this).addClass('active')
            }
        })
    }
});






