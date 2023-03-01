
from django.conf import settings
from django.shortcuts import redirect
from django.views.generic import View
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build

class GoogleCalendarInitView(View):
    def get(self, request):
        # Step 1: Authorization URL
        flow = Flow.from_client_config(
            settings.GOOGLE_OAUTH2_CLIENT_CONFIG,
            scopes=['https://www.googleapis.com/auth/calendar.events'],
            redirect_uri=request.build_absolute_uri('/rest/v1/calendar/redirect/')
        )
        authorization_url, _ = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true'
        )
        return redirect(authorization_url)

class GoogleCalendarRedirectView(View):
    def get(self, request):
        # Step 2: User authorization
        code = request.GET.get('code')
        flow = Flow.from_client_config(
            settings.GOOGLE_OAUTH2_CLIENT_CONFIG,
            scopes=['https://www.googleapis.com/auth/calendar.events'],
            redirect_uri=request.build_absolute_uri('/rest/v1/calendar/redirect/')
        )
        flow.fetch_token(code=code)

        # Step 3: Access token request
        credentials = flow.credentials
        service = build('calendar', 'v3', credentials=credentials)
        events = service.events().list(calendarId='primary').execute()

        # Step 4: Accessing the API
        return JsonResponse(events)
