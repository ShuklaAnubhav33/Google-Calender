from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.urls import reverse
from google.oauth2 import client
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class GoogleCalendarRedirectView(View):
    def get(self, request, *args, **kwargs):
        # Get the authorization code from the request
        auth_code = request.GET.get('code')
        if not auth_code:
            return HttpResponseBadRequest('Missing authorization code')

        # Set up the OAuth2 flow
        flow = client.OAuth2WebServerFlow(
            client_id=settings.GOOGLE_CLIENT_ID,
            client_secret=settings.GOOGLE_CLIENT_SECRET,
            scope=settings.GOOGLE_CALENDAR_SCOPE,
            redirect_uri=request.build_absolute_uri(reverse('google-calendar-redirect')),
            access_type='offline',
            prompt='consent'
        )

        # Exchange the authorization code for an access token
        try:
            credentials = flow.fetch_token(code=auth_code)
        except Exception as e:
            return HttpResponseBadRequest(f'Failed to fetch access token: {e}')

        # Save the credentials to the database or session
        # For this example, we'll just store the credentials in the session
        request.session['google_calendar_credentials'] = credentials.to_json()

        # Redirect to the events view
        return HttpResponseRedirect(reverse('google-calendar-events'))
