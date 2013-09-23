from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponseServerError
from django.core.urlresolvers import reverse
from django.views import generic

from polls.models import Poll, Choice


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_poll_list'

    def get_queryset(self):
        """Return the last five published polls."""
        return Poll.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Poll
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Poll
    template_name = 'polls/results.html'


def _mark_voted(request,poll_id):
    if not 'voted' in request.session:
        request.session['voted'] = []
    # Make sure the user can't vote again on this poll
    request.session['voted'].append(poll_id)


def vote(request, poll_id):
    p = get_object_or_404(Poll, pk=poll_id)
    if 'voted' in request.session and poll_id in request.session['voted']:
        # Display results page
        return HttpResponseServerError("You've already voted on this poll.")

    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return HttpResponseServerError("You didn't select a choice.")
    else:
        _mark_voted(request, poll_id)
        selected_choice.votes += 1
        selected_choice.save()

        if request.is_ajax():
            return render(request, 'polls/results.html', {
                'poll': p,
            })
        else:
            return HttpResponseRedirect(p.get_absolute_url())