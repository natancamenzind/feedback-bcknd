from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import CreateView, DetailView, UpdateView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import FormView

from dispatch_to_support.dispatcher import CustomerSupportDispatcher
from dispatch_to_support.forms import ResponseForm
from dispatch_to_support.models import Response, SupportTicket


# some debug
def sample_gen():
    i = 1
    while i:
        yield i
        i += 1

gen = sample_gen()
dispatcher = CustomerSupportDispatcher()
# Create your views here.
class QueueView(PermissionRequiredMixin, View):

    permission_required = [
        'dispatch_to_support.change_supportticket'
    ]

    raise_exception = True

    def get(self, request):
        return render(request, 'dispatch_to_support/get_case.html')

    def post(self, request):
        # return redirect()
        # dispatcher.populate_queue()
        sentiment, data = dispatcher.give_next_customer_case(give_to=self.request.user)
        feedback = data["feedback"]
        support_ticket = data["support_ticket"]
        context = {
            'gen': next(gen),
            'queue': dispatcher.queue.empty(),
            'sentiment': sentiment,
            'feedback': feedback,
        }
        # return render(request, 'dispatch_to_support/queue.html', context)
        try:
            return redirect('dispatch_to_support:ticket-update', pk=support_ticket.pk)
        except AttributeError:
            return render(request, 'dispatch_to_support/queue.html', context)


class SupportTicketDetailView(LoginRequiredMixin, DetailView):
    model = SupportTicket
    template_name = "dispatch_to_support/support_ticket_detail.html"

    # def get_context_data(self, **kwargs):
    #         # Call the base implementation first to get a context
    #         context = super(SupportTicketDetailView, self).get_context_data(**kwargs)
    #         # Add in a QuerySet of all the books
    #         customer = self.object.feedback.customer
    #         context['customer_past_ticket_list'] = SupportTicket.objects.filter(feedback__customer_pk=customer.pk)
    #         print(context['customer_past_ticket_list'])
    #         return context


class SupportTicketUpdateView(PermissionRequiredMixin, UpdateView):
    
    permission_required = [
        'dispatch_to_support.change_supportticket'
    ]
    raise_exception = True
    
    model = SupportTicket

    fields = [
        # 'status',
    ]
    template_name = "dispatch_to_support/support_ticket_update.html"
    success_url = reverse_lazy('dispatch_to_support:queue')

    def form_valid(self, form):
        form.instance.support_person = self.request.user
        form.instance.status = 1  # Closed
        form.instance.closed = timezone.localtime()
        return super(SupportTicketUpdateView, self).form_valid(form)
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(SupportTicketUpdateView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        customer = self.object.feedback.customer
        context['customer_past_ticket_list'] = SupportTicket.objects.filter(
            feedback__customer=customer, 
            status=1
            )
        print(context['customer_past_ticket_list'])
        return context
# from django.views.generic.edit import CreateView
# from myapp.models import Author

# class AuthorCreate(CreateView):
#     model = Author
#     fields = ['name']

#     def form_valid(self, form):
#         form.instance.created_by = self.request.user
#         return super(AuthorCreate, self).form_valid(form)

class DashboardView(LoginRequiredMixin, View):

    def get(self, request):
        ctx = {
            'open_tickets': self.request.user.supportticket_set.filter(status=0)  # get open tickets
        }
        return render(request, 'dispatch_to_support/dashboard.html', ctx)



# class ResponseCreateView(CreateView):
#     pk_url_kwarg = 'ticket_pk'
#     # success_url= redirect('dispatch_to_support:ticket-update', pk=object.get_object())
#     success_url= reverse_lazy('dispatch_to_support:dashboard')
#     model = Response
#     fields = [
#         'text',
#         # 'support_ticket',
#         # 'support_person',
#     ]
#     template_name = "dispatch_to_support/response_form.html"

#     def form_valid(self, form):
        
#         form.instance.support_person = self.request.user
#         form.instance.support_ticket = self.get_object()
#         return super(ResponseCreateView, self).form_valid(form)

#     def post(self, request, ticket_pk, *args, **kwargs):

#         return super(ResponseCreateView, self).post(request, *args, **kwargs)


class ResponseCreateView(FormView):
    template_name = "dispatch_to_support/response_form.html"
    form_class = ResponseForm
    success_url= reverse_lazy('dispatch_to_support:dashboard')

    # def form_valid(self, form):
    #     form.instance.support_person = self.request.user
    #     form.instance.support_ticket = self.request.ticket_pk
    #     return super(ResponseCreateView, self).form_valid(form) 

    def post(self, request, ticket_pk, *args, **kwargs):
        # def form_valid(self, form):
        #     form.instance.support_person = self.request.user
        #     form.instance.support_ticket = ticket_pk
        #     return super(ResponseCreateView, self).form_valid(form)
        form = ResponseForm(data=request.POST)
        form.instance.support_person = self.request.user
        form.instance.support_ticket = SupportTicket.objects.get(pk=ticket_pk)
        form.save()
        # return super(ResponseCreateView, self).post(request, *args, **kwargs) 
        return redirect('dispatch_to_support:ticket-update', pk=ticket_pk)


    # def post(self, request):
    #     form = UserAddForm(data=request.POST)
    #     if form.is_valid():
    #         User.objects.create_user(**form.cleaned_data)
    #         return redirect('exercises:user-login')
    #     else:
    #         return render(request, 'exercises/user_add_form.html', {'form': form})


class ResponseDetailView(DetailView):
    model = Response
    template_name = "dispatch_to_support/response_detail.html"
