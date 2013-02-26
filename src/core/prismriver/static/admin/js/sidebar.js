django.jQuery(document).ready(function() {
    django.jQuery(".app_title").click(function() {
        django.jQuery(this).parent().find("ul").slideToggle();
    });
});