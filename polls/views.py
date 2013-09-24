from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseServerError
from django.views import generic

from polls.models import Poll, Choice


class DetailView(generic.DetailView):
    model = Poll
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Poll
    template_name = 'polls/results.html'


# Gets a list of the latest polls and voted boolean for this user
def _get_polls_and_voted(request):
    polls = Poll.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:10]
    polls_voted = []
    for p in polls:
        t = p, ('voted' in request.session and unicode(p.id) in request.session['voted'])
        polls_voted.append(t)
    return polls_voted


# Make sure the user can't vote again on this poll
def _mark_voted(request, poll_id):
    if not 'voted' in request.session:
        request.session['voted'] = []
    voted_on = request.session['voted']
    voted_on.extend([poll_id])
    request.session['voted'] = voted_on


# Check if this user voted on the poll_id
def _has_user_voted(request, poll_id):
    return 'voted' in request.session and poll_id in request.session['voted']


# Front page (polls list)
def index(request):
    polls_voted = _get_polls_and_voted(request)
    return render(request, 'polls/index.html', {
        'latest_poll_list': polls_voted,
    })


# Save the user's vote on a poll
def vote(request, poll_id):
    try:
        p = get_object_or_404(Poll, pk=poll_id)
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        message = "You didn't select a choice."
    else:
        if 'voted' in request.session and poll_id in request.session['voted']:
            message = "You've already voted on this poll"
        else:
            message = "Thank you for voting, every vote counts!"
            _mark_voted(request, poll_id)
            selected_choice.votes += 1
            selected_choice.save()

    return render(request, 'polls/results_inner.html', {
        'poll': p,
        'message': message,
    })


# Create a new poll
def new(request):
    try:
        question = request.POST['question']
        choices = request.POST['choices'].split(',')
    except KeyError:
        return HttpResponseServerError("Missing some values.")
    else:
        p = Poll(question=question, pub_date=timezone.now())
        p.save()
        for choice in choices:
            Choice(poll=p, choice_text=choice, votes=0).save()

    polls_voted = _get_polls_and_voted(request)
    return render(request, 'polls/poll_list.html', {
        'latest_poll_list': polls_voted,
    })