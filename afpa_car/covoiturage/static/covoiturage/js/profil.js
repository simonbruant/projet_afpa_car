// Fonction d'affichage pour la side-bar

$(document).ready(function() {

    var navItems = $('.side-menu a');
    var allWells = $('.admin-contenu');
    var allWellsExceptFirst = $('.admin-contenu:not(:first)');

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