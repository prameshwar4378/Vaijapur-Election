 
from django.urls import path
from Myapp.views import *
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static 

urlpatterns = [
    # path('admin/', admin.site.urls),
    # path('candidates-api/', CandidateListView.as_view(), name='candidate-list'),
    # path('vote-api/', VoteCreateView.as_view(), name='vote-create'),
    # path('results-api/', VoteResultView.as_view(), name='vote-results'),
    path('', submit_vote, name='submit-vote'),
    path('result/',  vote_result, name='vote_result'),


]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)


