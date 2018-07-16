// Fonction d'affichage pour la side-bar

$(document).ready(function() {

    var navItems = $('.side-menu a');
    var allWells = $('.menu-contenu');
    var allWellsExceptFirst = $('.menu-contenu:not(:first)');

    allWellsExceptFirst.hide();

    navItems.click(function(e) {
        e.preventDefault();
        navItems.removeClass('active');
        $(this).closest('a').addClass('active');
    
    allWells.hide();
    var target = $(this).attr('data-target-id');
    $('#' + target).show();
    });
});

// Fonction affichage vehicule si oui 

