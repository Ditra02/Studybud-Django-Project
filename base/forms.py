from django.forms import ModelForm
from .models import Room, Message, User
from django.contrib.auth.forms import UserCreationForm

class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password1', 'password2']

class RoomForm(ModelForm):
    class Meta:
        model = Room  # model di tentukan untuk membuat form apa
        
        # ini akan membuat form berdasar pada data (metadata) dari Room yang ada di models.py kek host, topic dll
        # ini akan membuat host form field, dropdown list topic, text field untuk nama dan description
        # updated dan created tapi keduanya takkan tampil karena bukan field yang editable
        # fields = ['name', 'body'] # menentukan mana yang tampil 
        # fields = '__all__' # memberi kita semua fields data
        
        # fields = ['topic', 'name', 'description'] # memberi kita semua fields data
        
        fields = '__all__'
        exclude = ['host', 'participants']  # fields yang tak perlu di tampilkan 

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['avatar', 'name', 'username', 'email', 'bio']
