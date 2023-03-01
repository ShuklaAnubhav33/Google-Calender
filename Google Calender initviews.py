from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.urls import reverse
from google.oauth2 import client
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class GoogleCalendarInitView(View):
    def get(self, request, *args, **kwargs):
        # Set up the OAuth2 flow
        flow = client.OAuth2WebServerFlow(
            client_id=settings.GOOGLE_CLIENT_ID,
            client_secret=settings.GOOGLE_CLIENT_SECRET,
            scope=settings.GOOGLE_CALENDAR_SCOPE,
            redirect_uri=request.build_absolute_uri(reverse('google-calendar-redirect')),
            access_type='offline',
            prompt='consent'
        )
        # Generate the authorization URL
        auth_url, _ = flow.authorization_url(access_type='offline')
        return HttpResponseRedirect(auth_url)

