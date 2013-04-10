from django.contrib.sites.models import Site


def site(request):
    """
    Adds site-related context variables to the context.
    """
    current_site = Site.objects.get_current()

    return {
        'SITE_NAME': current_site.name,
        'SITE_DOMAIN': current_site.domain,
        'SITE_URL': "http://www.%s" % (current_site.domain),
    }
