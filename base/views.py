from django.shortcuts import render, redirect
from django.http import HttpResponse  # for test http response
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.forms import UserCreationForm
from .models import Room, Topic, Message, User   # importing the model
from .forms import RoomForm, UserForm, MyUserCreationForm
import datetime
from urllib.parse import quote_plus


def loginPage(request):
    page = 'login'
    
    # user belum login
    if not request.user.is_authenticated:

        if request.method == 'POST':
            email = request.POST.get('email').lower()
            password = request.POST.get('password')

            try:
                user = User.objects.get(email=email)
            except:
                messages.error(request=request, message='User does not exist')

            # givc us error or return User object that matches username and pass credentials
            user = authenticate(
                request=request, email=email, password=password)

            if user is not None:
                # add in the sessions in the database, then cookies in our browser
                login(request=request, user=user)
                return redirect('home')

            else:
                messages.error(request=request,
                               message='Username or Password does not exist')

        context = {'page': page}
        return render(request=request, template_name='base/login_register.html', context=context)

    # user udh login
    else:
        return redirect('home')


def logoutUser(request):
    # it wll delete the token in the cookies in browser
    logout(request=request)
    return redirect('home')


def registerPage(request):
    if not request.user.is_authenticated:
        page = 'register'
        form = MyUserCreationForm()

        if request.method == 'POST':
            form = MyUserCreationForm(request.POST)

            if form.is_valid():
                user = form.save(commit=False)  #
                user.username = user.username.lower()
                user.save()

                login(request=request, user=user)
                return redirect('home')

            else:
                messages.error(request=request,
                            message='An error occured during registration')

        context = {'page': page, 'form': form}
        return render(request=request, template_name='base/login_register.html', context=context)
    
    else:
        return redirect('home')


# request objek : the http objek is gooing to tell us what kind of request method is sent. What kind of data is being passed in. What's the user sending to the backend
def home(request):
    # model manager (querysets), give us all the room in database
    # Room.objects.all().delete()
    # rooms = Room.objects.all()

    q = quote_plus(request.GET.get('q')) if request.GET.get(
        'q') != None else ''  # quote plus untuk handle jika ada symbol

    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )

    topics = Topic.objects.all()[0:5]
    room_count = rooms.count()
    room_messages = Message.objects.filter(
        Q(room__name__icontains=q) |
        Q(room__topic__name__icontains=q)
    )

    context = {'rooms': rooms,
               'topics': topics,
               'room_count': room_count,
               'room_messages': room_messages
               }

    # request : http request, how we pass data back and forth
    return render(request=request, template_name='base/home.html', context=context)


def room(request, pk):
    room = Room.objects.get(id=pk)
    # you can see the message_set with help(room), order in descending, many to one relationship
    room_messages = room.message_set.all().order_by('-created')
    participants = room.participants.all()

    if request.method == "POST":
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )

        # participants bertambah jika user kirim message
        room.participants.add(request.user)
        return redirect('room', pk=room.id)

    context = {'room': room, 'room_messages': room_messages,
               'participants': participants}
    return render(request=request, template_name='base/room.html', context=context)


def userProfile(request, pk):
    user = User.objects.get(id=pk)
    topics = Topic.objects.all()
    room_messages = user.message_set.all()

    q = request.GET.get('q') if request.GET.get('q') != None else ''

    rooms = user.room_set.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q)
    )  # get all spesific children

    # loop untuk mencari tau jumlah room pada masing2 topic yang dimiliki user
    room_in_topic = {}

    for topic in topics:
        room_in_topic[topic.name] = user.room_set.filter(topic=topic).count()

    context = {
        'user': user,
        'rooms': rooms,
        'room_messages': room_messages,
        'topics': topics,
        'profile_page': True,
        'room_in_topic': room_in_topic
    }
    return render(request=request, template_name='base/profile.html', context=context)


@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()

    if request.method == "POST":

        topic_name = request.POST.get('topic')

        # jika ada topic akan return topic yg ada dan created bernilai False
        # jika topic tidak ada maka topic baru terbentuk, topic return topic yang baru terbentuk dan created akan True
        topic, created = Topic.objects.get_or_create(name=topic_name)
        Room.objects.create(
            host=request.user,
            topic=topic,
            # this name come from {{ form.name }}
            name=request.POST.get('name'),
            description=request.POST.get('description'),
        )
        return redirect('home')

    context = {
        'form': form,
        'topics': topics
    }
    return render(request=request, template_name='base/room_form.html', context=context)


@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()

    if request.user != room.host:
        return HttpResponse('You are now allowed here!!')

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, create = Topic.objects.get_or_create(name=topic_name)
        room.topic = topic
        room.name = request.POST.get('name')
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')

    context = {'form': form,
               'topics': topics,
               'room': room}

    return render(request=request, template_name='base/room_form.html', context=context)


@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse('You are not allowed here!!')

    if request.method == 'POST':
        room.delete()
        next_page = request.POST.get('next')
        return redirect(next_page)

    return render(request=request, template_name='base/delete.html', context={'obj': room})


@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('You are not allowed here!!')

    if request.method == 'POST':
        message.delete()

        # mengarahkan ke page asal sebelum ke menu delete
        next_page = request.POST.get('next')
        return redirect(next_page)

    return render(request=request, template_name='base/delete.html', context={'obj': message})


@login_required(login_url='login')
def updateMessage(request, pk):
    message = Message.objects.get(id=pk)  # ambil message yang di update
    body = message.body  # body, untuk di pass in ke html

    # ambil room dimana message berada
    room = Room.objects.get(id=message.room_id)
    # ambil semua message pada room dengan relasi one-to-many
    room_messages = room.message_set.all()
    # ambil semua participants yang ada dalam room dengan relasi many-to-many
    participants = room.participants.all()

    if request.user != message.user:
        return HttpResponse('You are not allowed here!!')

    if request.method == 'POST':
        message.body = request.POST.get('body')     # update komen
        message.save()
        return redirect('room', pk=message.room_id)

    context = {
        'updating_message': True,
        'message_updated_id': pk,
        'room': room,
        'room_messages': room_messages,
        'body': body,
        'participants': participants,
    }

    return render(request=request, template_name='base/room.html', context=context)


@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == "POST":
        # request.FILES it will send the files with it and actually process that 
        form = UserForm(data=request.POST, files=request.FILES, instance=user)

        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)

    context = {'form': form}
    return render(request=request, template_name='base/update-user.html', context=context)


def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    topics = Topic.objects.filter(name__icontains=q)
    context = {'topics': topics}
    return render(request=request, template_name='base/topics.html', context=context)


def activityPage(request):
    room_messages = Message.objects.all()

    context = {'activities': room_messages}

    return render(request=request, template_name='base/activity.html', context=context)


def test(request):
    user = User.objects.get(email='azaleapansy@gmail.com')

    # user = authenticate(request=request, email='azaleapansy@gmail.com', password='adminpanel02')

    context = {
        'user': user
    }
    return render(request, 'base/test.html', context=context)
