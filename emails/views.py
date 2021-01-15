from django.shortcuts import render
from .forms import EmailForm
from .models import Email
from .sheets import update_sheet
from .emailer import send_to_everyone, send_verification
from . import url

# Create your views here.
"""
def subscribe_view(request):
    form = EmailForm()

    if request.method == "POST":
        form = EmailForm(request.POST)
        if form.is_valid():
            if form.cleaned_data["email"] not in map(lambda x: x, Email.objects.values()):
                Email.objects.create(**form.cleaned_data)
                form = EmailForm()

    context = {
        "form": form
    }
    return render(request, "emails/subscribe.html", context)
"""

base_url = url.base_url

def subscribe_view(request):
    form = EmailForm(request.POST or None)
    if form.is_valid():
        form.save()
        form = EmailForm()
        send_verification(request.POST["email"])
        update_sheet() # Ez a functoion sokáig tart, úgyhogy érdemes threading-el csinálni majd
        subscribed = 2
    else: 
        if request.method == "POST":
            subscribed = 1
        else:
            subscribed = 0

    context = {
        "form": form,
        "subscribed": subscribed
    }

    return render(request, "emails/subscribe.html", context)

def send_to_everyone_view(request):
    send_to_everyone()
    context = {
        "base_url": base_url
    }
    return render(request, "emails/sendtoeveryone.html", context)

def unsibscribe_view(request):

    if list(request.GET.keys()) == []:
        context = {
            "base_url": base_url,
            "fail": False
        }
        return render(request, "emails/unsubscribe.html", context)
    else:
        email = request.GET["email"]
        found = False
        for d in Email.objects.values():
            if d['email'] == email:
                found = True
                id = d['id']
                break
        
        if found:
            obj = Email.objects.get(id=id)
            obj.delete()
            update_sheet()
            context = {
                "base_url": base_url,
            }
            return render(request, "emails/unsubscribed.html", context)
        else:
            context = {
                "base_url": base_url,
                "fail": True
            }
            return render(request, "emails/unsubscribe.html", context)