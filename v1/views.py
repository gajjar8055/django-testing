from v1.models import Question, Choice, CPU
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from .forms import NameForm, ContactForm
import json
from django.core.mail import send_mail


def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'v1/index.html', context)


def detail(request, question_id):
    def detail(request, question_id):
        question = get_object_or_404(Question, pk=question_id)
        return render(request, 'v1/detail.html', {'question': question})


def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'v1/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


def get_name(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ContactForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            sender = form.cleaned_data['sender']
            cc_myself = form.cleaned_data['cc_myself']

            recipients = ['info@example.com']
            if cc_myself:
                recipients.append(sender)
            print(subject, message, sender, recipients)
            # send_mail(subject, message, sender, recipients)
            return HttpResponseRedirect('/thanks/')

    else:
        form = ContactForm()

    return render(request, 'name.html', {'form': form})


def scarping(request):
    if request.method == "GET":

        import requests
        data = {}
        html_data = ""
        for i in range(1, 11):
            respo = requests.get(
                'https://pcpartpicker.com/products/cpu/fetch/?page=' + str(i) + '&mode=list&xslug=&search=')
            print('https://pcpartpicker.com/products/cpu/fetch/?page=' + str(i) + 'mode=list&xslug=&search=')
            json_out = respo.json()
            data.update(json_out['result']['data'])
            html_data = html_data + str(json_out['result']['html'])

            for i, k in data.items():
                cpu_daya = CPU.objects.filter(ref_id=data[i]['id'])
                if cpu_daya.exists():
                    cpu_daya.update(slug=data[i]['slug'], name=data[i]['name'], grouped=data[i]['grouped'],
                                    price=data[i]['price'])
                else:

                    CPU.objects.create(slug=data[i]['slug'], name=data[i]['name'], grouped=data[i]['grouped'],
                                       price=data[i]['price'], ref_id=data[i]['id'])

        return HttpResponse(content_type="application/json", content="{}")


def update_cpu_link(request):
    if request.method == "GET":
        from bs4 import BeautifulSoup

        file_ht = open('/Users/ahesanali/PycharmProjects/DjangoTest/templates/CPU_html.html')

        bs_data = BeautifulSoup(file_ht.read(), 'html.parser')
        links_data = bs_data.find_all('tr')
        for i in links_data:
            first = i.find_next("td")
            second = first.find_next("td")
            print("First", first.input['id'], "second", second.a['href'])
            cpus = CPU.objects.filter(ref_id=str(first.input['id'])[3:], )
            if cpus.exists():
                cpus.update(link_name=second.a['href'])
