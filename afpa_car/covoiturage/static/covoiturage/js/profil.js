// Fonction d'affichage pour la side-bar

$(document).ready(function() {

    // VERSION INITIAL
    // var tableau =  $("#filtre_url_contenu a")

    // tableau.each(element => {
    //      if (tableau[element].href == document.location.href)
    //      {
    //         tableau.eq(element).addClass('active');
    //      }
    //  });


    $("#filtre_url_contenu a").each(function( index ) {
        if ( this.href == document.location.href)
        {             
            $(this).addClass('active');
        }
    })
});



 


