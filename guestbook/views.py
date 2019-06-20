from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from guestbook.models import Guestbook


def list(request):
    if request.method == "GET":
        guestbooks = Guestbook.objects.all().order_by('-id')
        data = {'guestbooks': guestbooks}
        # 객체를 담아서 view로 보내는 방법은 객체를 dict로 담아서 return 시 넘겨주면 된다.
        return render(request, 'guestbook/list.html', data)

    elif request.method == "POST":
        guestbook = Guestbook()
        guestbook.name = request.POST['name']
        guestbook.password = request.POST['password']
        guestbook.content = request.POST['content']

        guestbook.save()
        return HttpResponseRedirect('/guestbook')


def delete(request, id=0):
    if request.method == "GET":
        data = {'id': id}
        return render(request, 'guestbook/deleteform.html', data)

    elif request.method == "POST":
        password = request.POST['password']
        guestbook = Guestbook.objects.filter(id=id).filter(password=password)
        guestbook.delete()
        return HttpResponseRedirect('/guestbook')
