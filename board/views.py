from math import ceil, floor

from django.core.paginator import Paginator

import board as board
from django.db.models import Max, F
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

# Create your views here.
from board.models import Board
from user.models import User


def pagernation(page, item_list, page_per_screen=5, item_per_page=10):
    total_item_no = len(item_list)
    total_page_no = round(total_item_no / item_per_page) + 1
    start_item_no = (int(page) - 1) * item_per_page
    end_item_no = start_item_no + item_per_page
    result = {'total_item_no': int(total_item_no),
              'total_page_no': int(total_page_no),
              'start_item_no': int(start_item_no),
              'end_item_no': int(end_item_no)}
    return result


def list(request, page):
    q = request.GET.get('q','')

    page_per_screen = 5
    board_per_page = 10
    total_item_no = Board.objects.count()
    total_page_no = ceil(total_item_no / board_per_page) + 1
    start_item_no = (int(page) - 1) * board_per_page
    end_item_no = start_item_no + board_per_page
    page_view = floor((int(page)-1)/int(page_per_screen)) * page_per_screen
    board_list = Board.objects.all().order_by('-groupno', 'orderno', 'depth')
    if q:
      board_list=board_list.filter(title=q)[start_item_no:start_item_no +  board_per_page]
    board_list = board_list[start_item_no:start_item_no + board_per_page]
    data = {'board_list':board_list,
            'page_per_screen': int(page_per_screen),
            'page': int(page),
            'total_item_no': int(total_item_no),
            'total_page_no': int(total_page_no),
            'start_item_no': int(start_item_no),
            'end_item_no': int(end_item_no),
            'page_view' : int(page_view),
            'q':q
            }
    return render(request, 'board/list.html', data)


def modify(request, id=0):
    board = Board.objects.get(id=id)
    if check_sameuser(request, board):
        if request.method=='GET':
            data={
                'board': board
            }
            return render(request, 'board/modify.html', data)
        elif request.method =='POST':
            board.title = request.POST['title']
            board.content = request.POST['content']
            board.save()
            return HttpResponseRedirect(f'/board/view/{id}?result=success')
    else:
        return HttpResponseRedirect(f'/board/view/{id}?result=fail')


def view(request, id=0):
    board=Board.objects.get(id=id)
    data = {
        'board':board
    }
    board.hit = board.hit + 1
    board.save()
    return render(request, 'board/view.html', data)


def write(request):
    if check_authuser(request) is None:
        return HttpResponseRedirect('/user/loginform')
    else:
        if request.method=='GET':
            return render(request, 'board/write.html')
        elif request.method =='POST':
            value = Board.objects.aggregate(max_groupno=Max('groupno'))
            max_groupno = 0 if value["max_groupno"] is None else value["max_groupno"]
            board = Board()
            board.title = request.POST['title']
            board.content = request.POST['content']
            board.user = User.objects.get(id=request.session['authuser']['id'])
            board.groupno = max_groupno+1
            board.save()
            return HttpResponseRedirect('/board/1')


def delete(request, id=0):
    board = Board.objects.get(id=id)
    if check_sameuser(request,board) :
        board.delete()
        return HttpResponseRedirect('/board/1?result=success')
    else:
        return HttpResponseRedirect('/board/1?result=fail')


def reply(request, id=0):
    # 로그인 체크
    if check_authuser(request) is None:
        return HttpResponseRedirect('/user/loginform')
    else:
        if request.method == 'GET':
            return render(request, 'board/write.html')
        elif request.method == 'POST':
            board = Board.objects.get(id=id)
            # query set 예제
            # groupno = 1이고 orderno >=1 의
            # 게시물의 order_no를 1씩 증가
            # __gt, __lt, __gte, __lte
            reply_board = Board()
            reply_board.title = request.POST['title']
            reply_board.content = request.POST['content']
            reply_board.user = User.objects.get(id=request.session['authuser']['id'])
            reply_board.groupno = board.groupno
            # value = Board.objects.filter(groupno=board.groupno).filter(depth=board.depth+1).aggregate(max_orderno=Max('orderno'))
            # max_orderno = 0 if value["max_orderno"] is None else value["max_orderno"]
            reply_board.orderno = board.orderno + 1
            reply_board.depth = board.depth + 1
            reply_board.save()
            # Board.objects.filter(groupno=board.groupno).filter(orderno=board.orderno).update(depth=F('depth') + 1)
            return HttpResponseRedirect('/board/1')


def check_authuser(request):
    try:
        authuser = User.objects.get(id=request.session['authuser']['id'])
    except Exception as e:
        authuser = None
    return authuser

def check_sameuser(request, board):
    if board.user.id == check_authuser(request).id:
        sameuser = True
    else :
        sameuser = False
    return sameuser