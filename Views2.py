import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from django.conf import settings
from django.http import JsonResponse
from django.urls import reverse
from django.views import View


class GoogleCalendarInitView(View):
    def get(self, request):
        flow = Flow.from_client_config(
            settings.GOOGLE_OAUTH2_CLIENT_CONFIG,
            scopes=['https://www.googleapis.com/auth/calendar.events.readonly'],
            redirect_uri=request.build_absolute_uri(reverse('calendar_redirect'))
        )

        auth_url, _ = flow.authorization_url(prompt='consent')

        return JsonResponse({'auth_url': auth_url})


class GoogleCalendarRedirectView(View):
    def get(self, request):
        flow = Flow.from_client_config(
            settings.GOOGLE_OAUTH2_CLIENT_CONFIG,
            scopes=['https://www.googleapis.com/auth/calendar.events.readonly'],
            redirect_uri=request.build_absolute_uri(reverse('calendar_redirect'))
        )

        code = request.GET.get('code', '')
        flow.fetch_token(code=code)

        credentials = flow.credentials
        service = build('calendar', 'v3', credentials=credentials)

        events = service.events().list(calendarId='primary').execute()

        return JsonResponse({'events': events})

