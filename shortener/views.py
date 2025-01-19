from datetime import timedelta
from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.timezone import now
from .models import URL, Analytics
import hashlib
from django.views.decorators.csrf import csrf_exempt


def generate_short_url(long_url):
    return hashlib.md5(long_url.encode()).hexdigest()[:6]

@csrf_exempt
def shorten_urls(request):
    if request.method == 'POST':
        data = request.POST
        original_url = data.get('url')
        expiry_hours = int(data.get('expiry_hours', 24))

        if not original_url:
            return JsonResponse({'error': 'URL is required.'}, status=400)

        short_url = generate_short_url(original_url)
        expires_at = now() + timedelta(hours=expiry_hours)
        url, created = URL.objects.get_or_create(
            original_url=original_url,
            defaults={'short_url': short_url, 'expires_at': expires_at}
        )
        return JsonResponse({'short_url': f'/r/{url.short_url}', 'expires_at': url.expires_at.isoformat()})
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=405)


def redirect_url(request, short_url):
    url = get_object_or_404(URL, short_url=short_url)

    if now() > url.expires_at:
        return HttpResponse("URL expired", status=410)

    Analytics.objects.create(short_url=url, ip_address=get_client_ip(request))
    return HttpResponseRedirect(url.original_url)


def get_analytics(request, short_url):
    url = get_object_or_404(URL, short_url=short_url)
    logs = Analytics.objects.filter(short_url=url).values('accessed_at', 'ip_address')
    return JsonResponse({'short_url': url.short_url, 'logs': list(logs)})


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0]
    return request.META.get('REMOTE_ADDR')
