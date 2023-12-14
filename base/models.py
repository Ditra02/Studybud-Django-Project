from django.db import models
# from django.contrib.auth.models import User # default django user model
import datetime
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(null=True, unique=True)
    bio = models.TextField(null=True)

    # default parameter is the default picture
    avatar = models.ImageField(
        null=True, default="avatar.svg")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.name


# it's created because the Room Class will be the child of the Topic Class
# a topic can have mulitple rooms
class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

# room class inherit from models, 'models' akan mengubah class python standar menjadi django model


class Room(models.Model):

    # the actual user to be connected
    # somebody has to host the room
    # ini tidak ada di Room.objects.all().values() karena reference dari user, bisa dilihat di django admin panel User
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    # a room can only have one topic
    # on_delete = models.SET_NULL : if topic deleted then the room doesn't deleted, The topic will set to null
    # ini tidak ada di Room.objects.all().values() karena reference dari class Topic
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)

    # Character Field, it's a text field , Anda harus menentukan attribut dan tipenya
    # the max length adalah untuk mengatur panjang character maximal
    name = models.CharField(max_length=200)

    # TextField adalah text field yang lebih besar
    # null = True, memungkinkan data bernilai null
    # blank = True, ketika kita menjalankan metode save seperti submit form, formnya bisa disimpan dengan kosong
    description = models.TextField(null=True, blank=True)

    # menyimpan semua user yang aktif di room
    # jadi jika Anda komen di sebuah room berari Anda adalah participant
    participants = models.ManyToManyField(
        User, related_name='participants', blank=True)

    # Take a snapshot setiap waktu model di perbarui
    # jadi kapanpun kita menjalankan metode save untuk update model ini atau spesifik tabel atau item
    # auto_now (True) : menyimpan time stamp setiap data di perbarui
    updated = models.DateTimeField(auto_now=True)

    # auto_now_add (True) : hanya menyimpan time stamp ketika instance pertama kali dibuat
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        # There's other value we can set

        # first item in this list are going to prioritized and then it's going chain on down that way
        # the order here based on data recently that updated or created
        # without the dash it will sorted in ascending order
        # '-' or dash means it will sorted in descending order
        ordering = ['-created', '-updated']

    # id =

    # ini akan menampilkan nama dari objek di page http://127.0.0.1:8000/admin/base/room/
    # jika tidak ada akan tampil Room object (1), dst
    def __str__(self) -> str:
        return str(self.name)

# each room should have message


class Message(models.Model):

    # one to many relationship, user can have many messages, a message can only have one user
    # on_delete = models.CASCADE, if a user is delete, it will delete all the children
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # on_delete : models.SET_NULL, imagine when someone deletes this room what we gonna do with the children is set to null value
    # on_delete : models.CASCADE, when a room is deleted, all children (messages) also deleted
    # parent : Room, child = Message
    room = models.ForeignKey(Room, on_delete=models.CASCADE)

    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created', '-updated']

    def __str__(self):
        # trim only 50 characters in the preview django admin panel
        return self.body[0:50]
