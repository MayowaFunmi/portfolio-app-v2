from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import redirect, render
from users.models import UserAccount as User
from .models import Room, PrivateChat, Message
from django.views import View


# homepage
@login_required
def home(request):
    all_users = User.objects.all
    all_rooms = Room.objects.all()
    if request.method == 'POST':
        room_username = request.user.username
        user_room_name = request.POST['room_name']
        room_name = user_room_name.lower()
        username = room_username.lower()

        if Room.objects.filter(name=room_name).exists():
            return redirect('/chat/'+room_name+'/'+username+'?chat room name='+room_name+' '+'username='+username)
        else:
            new_room = Room.objects.create(name=room_name, created_by=request.user)
            new_room.save()
            return redirect('/chat/'+room_name+'/'+username+'?chat room name='+room_name+' '+'username='+username)
    context = {
        'all_users': all_users,
        'all_rooms': all_rooms
    }
    return render(request, 'chat/home.html', context)


@login_required
def enter_room(request):
    if request.method == 'POST':
        room_username = request.user.username
        user_room_name = request.POST['select_room']
        room_name = user_room_name.lower()
        username = room_username.lower()
        return redirect('/chat/' + room_name + '/' + username + '?chat room name=' + room_name + ' ' + 'username=' + username)


@login_required
def room(request, room_name, username):
    room_details = Room.objects.filter(name=room_name)
    context = {
        'room_name': room_name,
        'room_details': room_details,
        'username': username
    }
    return render(request, 'chat/room.html', context)


class GetMessages(LoginRequiredMixin, View):
    def get(self, request):
        room_name = request.GET.get('room_name')
        room_msg = Message.objects.filter(room__name=room_name)[:30]
        messages = []
        data = {}
        for i in range(len(room_msg)):
            x = room_msg[i].date
            datex = x.strftime("%d-%m-%Y")
            timex = x.strftime("%H:%M:%S %p")
            date_sent = datex+' '+'at'+' '+timex

            msg = {
                'id': room_msg[i].id,
                'user': room_msg[i].user.username,
                'room_name': room_msg[i].room.name,
                'message': room_msg[i].message,
                'date': date_sent,
            }
            messages.append(msg)
        data['message_details'] = messages
        return JsonResponse(data)


class SaveMessages(LoginRequiredMixin, View):
    def get(self, request):
        username = request.GET.get('username', None)
        room_id = request.GET.get('room_id', None)
        message = request.GET.get('message', None)

        chat_room = Room.objects.get(id=room_id)
        obj = Message.objects.create(
            user=request.user,
            room=chat_room,
            message=message,
        )
        message_details = {
            'id': obj.id,
            'user': request.user.first_name+' '+request.user.last_name,
            'room_name': obj.room.name,
            'room_creator': chat_room.created_by,
            'message': obj.message,
            'date': obj.date
        }
        data = {
            'message_details': message_details
        }
        return JsonResponse(data)


def private_chat(request):
    sender_x = request.user.username
    receiver_x = request.POST['receiver']
    sender = sender_x.lower()
    receiver = receiver_x.lower()
    if sender == receiver:
        messages.error(request, 'You cannot chat with yourself')
        return redirect('chat:home')
    return redirect('/chat/private/' + sender + '/' + receiver + '?private chat between ' + sender + 'and ' + receiver)


def private(request, sender, receiver):
    chat_details = PrivateChat.objects.filter(sender__username=sender, receiver__username=receiver)
    context = {
        'sender': sender,
        'receiver': receiver,
        'chat_details': chat_details
    }
    return render(request, 'chat/private_chat.html', context)


class SavePrivate(LoginRequiredMixin, View):
    def get(self, request):
        sender = request.GET.get('sender', None)
        user_rec = request.GET.get('receiver', None)
        message = request.GET.get('message', None)
        receiver = User.objects.get(username=user_rec)

        obj = PrivateChat.objects.create(
            sender=request.user,
            receiver=receiver,
            message=message
        )
        private_msg = {
            'id': obj.id,
            'sender': request.user.username,
            'receiver': user_rec,
            'message': obj.message,
            'date': obj.date
        }
        data = {
            'private_msg': private_msg
        }
        return JsonResponse(data)


class GetPrivate(LoginRequiredMixin ,View):
    def get(self, request):
        sender = request.GET.get('sender', None)
        receiver = request.GET.get('receiver', None)
        messages = []
        data = {}
        # user_sender = User.objects.get(username=sender)
        # user_receiver = User.objects.get(username=receiver)
        # print('sender = ', user_sender)
        # print('receiver = ', user_receiver)
        if PrivateChat.objects.filter(sender__username=sender, receiver__username=receiver).exists():
            pri_msg = PrivateChat.objects.filter(sender__username=sender, receiver__username=receiver)[:30]

            for i in range(len(pri_msg)):
                x = pri_msg[i].date
                datex = x.strftime("%d-%m-%Y")
                timex = x.strftime("%H:%M:%S %p")
                date_sent = datex + ' ' + 'at' + ' ' + timex

                msg = {
                    'id': pri_msg[i].id,
                    'message': pri_msg[i].message,
                    'date': date_sent,
                    'sender': sender,
                    'receiver': receiver
                }
                messages.append(msg)
        if PrivateChat.objects.filter(sender__username=receiver, receiver__username=sender).exists():
            pri_msg = PrivateChat.objects.filter(sender__username=receiver, receiver__username=sender)[:30]
            for i in range(len(pri_msg)):
                x = pri_msg[i].date
                datex = x.strftime("%d-%m-%Y")
                timex = x.strftime("%H:%M:%S %p")
                date_sent = datex + ' ' + 'at' + ' ' + timex

                msg = {
                    'id': pri_msg[i].id,
                    'message': pri_msg[i].message,
                    'date': date_sent,
                    'sender': sender,
                    'receiver': receiver
                }
                messages.append(msg)
        data['private_details'] = messages
        return JsonResponse(data)

