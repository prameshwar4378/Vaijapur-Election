from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Candidate, Vote
from .serializers import CandidateSerializer, VoteSerializer
from django.db.models import Count

class CandidateListView(APIView):
    def get(self, request):
        candidates = Candidate.objects.all()
        serializer = CandidateSerializer(candidates, many=True)
        return Response(serializer.data)

class VoteCreateView(APIView):
    def post(self, request):
        ip_address = request.META.get('REMOTE_ADDR')  # Get IP address from the request
        candidate_id = request.data.get('candidate_id')

        # Check if the IP has already voted
        if Vote.objects.filter(ip_address=ip_address).exists():
            return Response({"error": "You alredy voted on this poll."}, status=status.HTTP_403_FORBIDDEN)

        try:
            candidate = Candidate.objects.get(id=candidate_id)
        except Candidate.DoesNotExist:
            return Response({"error": "Candidate not found."}, status=status.HTTP_404_NOT_FOUND)

        # Create vote
        vote = Vote.objects.create(candidate=candidate, ip_address=ip_address)
        return Response({"message": "Vote submitted successfully."}, status=status.HTTP_201_CREATED)

class VoteResultView(APIView):
    def get(self, request):
        results = Candidate.objects.annotate(vote_count=Count('votes')).order_by('-vote_count')
        data = [{"name": candidate.name, "votes": candidate.vote_count} for candidate in results]
        return Response(data)






from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Candidate, Vote
from .forms import VoteForm
 

import random

def submit_vote(request):

#     candidate_ids = 3

# # Generate 30+ random votes for each candidate
    
#     candidate = Candidate.objects.get(id=candidate_ids)
#     num_votes = 570  # Randomize number of votes between 30 and 50
#     for _ in range(num_votes):
#         Vote.objects.create(
#             candidate=candidate,
#             ip_address=f"192.168.1.{random.randint(1, 255)}"  # Random dummy IPs
#         )
#     print("Dummy votes added for candidates 3, 4, and 5!")


    ip_address = get_client_ip(request)
    # Check if the IP has already voted
    if Vote.objects.filter(ip_address=ip_address).exists():
        return redirect('/result')

    candidates = Candidate.objects.all()
    if request.method == "POST":
        selected_candidate_id = request.POST.get('candidate')
        if not selected_candidate_id:
            return HttpResponse("Please select a candidate.", status=400)

        candidate = Candidate.objects.get(id=selected_candidate_id)
        Vote.objects.create(candidate=candidate, ip_address=ip_address)
        return redirect('/result')

    return render(request, 'submit_vote.html', {'candidates': candidates})

def get_client_ip(request):
    """Helper function to retrieve the client's IP address."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip




def vote_result(request):
    ip_address = get_client_ip(request)
    msg = "You already voted on this poll."

    # Fetch vote results
    candidates = Candidate.objects.all()
    total_votes = Vote.objects.count()

    # Process candidates and calculate votes and percentage
    candidates_list = []
    for candidate in candidates:
        candidate_votes = Vote.objects.filter(candidate=candidate).count()
        percentage = (candidate_votes / total_votes) * 100 if total_votes > 0 else 0
        candidates_list.append({
            'name': candidate.name,
            'photo': candidate.photo.url,
            'votes': candidate_votes,
            'percentage': round(percentage, 2),
        })

    # Sort candidates by votes in descending order for ranking
    candidates_list = sorted(candidates_list, key=lambda x: x['votes'], reverse=True)

    # Handle ranking with ties
    rank = 1
    for idx, candidate in enumerate(candidates_list):
        if idx > 0 and candidate['votes'] < candidates_list[idx - 1]['votes']:
            rank = idx + 1
        candidate['rank'] = rank

    # Assign colors dynamically
    color_palette = ['green', 'orange', 'blue', 'red', 'purple', 'yellow']
    for idx, candidate in enumerate(candidates_list):
        candidate['color'] = color_palette[idx % len(color_palette)]

    # Return data to template
    return render(request, 'vote-result.html', {
        'msg': msg,
        'candidates': candidates_list,
        'total_votes': total_votes,
    })


    
