from django.contrib.auth.decorators import login_required
from django.contrib.sessions.models import Session
from django.core.urlresolvers import reverse
from django.http import Http404
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DetailView, ListView
from django.core.exceptions import ValidationError

from .forms import BookingForm
from .models import Booking


class BookingViewMixin(object):
    model = Booking
    form_class = BookingForm


class BookingCreateView(BookingViewMixin, CreateView):
    """View to create a new ``Booking`."""
    def get_success_url(self):

        return reverse('booking_detail', kwargs={'pk': self.object.pk})

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(BookingCreateView, self).get_form_kwargs(
            *args, **kwargs)
        if 'data' in kwargs:
            count = list(Booking.objects.filter(date_from=kwargs['data']['date_from']))
            if count > 20:
                raise ValidationError("Sorry!!!. There are no rooms available for selected dates.")
        if self.request.user.is_authenticated():
            kwargs.update({'user': self.request.user})
        else:
            # If the user is not authenticated, get the current session
            if not self.request.session.exists(
                    self.request.session.session_key):
                self.request.session.create()
            kwargs.update({'session': Session.objects.get(
                session_key=self.request.session.session_key)})
        return kwargs


class BookingDetailView(BookingViewMixin, DetailView):

    def dispatch(self, request, *args, **kwargs):
        self.kwargs = kwargs
        self.object = self.get_object()
        if request.user.is_authenticated():
            # If user doesn't own the booking forbid access
            if not self.object.user == request.user:
                raise Http404
        else:
            # If anonymous doesn't own the booking forbid access
            session = self.object.session
            if (not session or not request.session.session_key or
                    session.session_key != request.session.session_key):
                raise Http404
        return super(BookingViewMixin, self).dispatch(request, *args, **kwargs)


class BookingListView(BookingViewMixin, ListView):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(BookingViewMixin, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return self.request.user.bookings.all()
