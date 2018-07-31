/* ###### Fonction d'affichage pour la side-bar ###### */
$(document).ready(function() {
     $("#filtre_url_contenu a").each(function( index ) {
        if ( this.href == document.location.href)
        {             
            $(this).addClass('active');
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



 


