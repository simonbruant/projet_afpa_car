/* ###### Fonction d'affichage pour la side-bar ###### */
$(document).ready(function () {
    $("#filtre_url_contenu a").each(function (index) {
        if (this.href == document.location.href) {
            $(this).addClass('active')
        }
        /* adresses */
        else if (this.href == document.location.href.substr(0, 40)) {
            $(this).addClass('active')
        }
        /* vehicule */
        else if (this.href == document.location.href.substr(0, 41)) {
            $(this).addClass('active')
        }
    })
});

/* ###### Vue.Js pour les préférences ###### */
new Vue({
    el: '#choice_smoker',
    data: {
        selected: undefined
    }
});

new Vue({
    el: '#choice_talker',
    data: {
        selected: undefined
    }
});

new Vue({
    el: '#choice_music',
    data: {
        selected: undefined
    }
});

/* ###### Vue.Js pour l'aperçu de l'Avatar ###### */
new Vue({
    el: '#preview_avatar',
    data: {
        imageData: ""  // we will store base64 format of image in this string
    },
    methods: {
        previewImage: function (event) {
            // Reference to the DOM input element
            var input = event.target;
            // Ensure that you have a file before attempting to read it
            if (input.files && input.files[0]) {
                // create a new FileReader to read this image and convert to base64 format
                var reader = new FileReader();
                // Define a callback function to run, when FileReader finishes its job
                reader.onload = (e) => {
                    // Note: arrow function used here, so that "this.imageData" refers to the imageData of Vue component
                    // Read image as base64 and set to imageData
                    this.imageData = e.target.result;
                }
                // Start the reader job - read file as a data url (base64 format)
                reader.readAsDataURL(input.files[0]);
            }
        }
    }
});

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



