from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('login/',views.login,name='login'),
    path('register/',views.register,name='register'),
    path('logout/', views.logout, name='logout'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('add_note/', views.add_note, name='add_note'),
    path('my_notes/', views.my_notes, name='my_notes'),
    path('edit_note/<int:note_id>/', views.edit_note, name='edit_note'),
    path('toggle_pin/<int:note_id>/', views.toggle_pin, name='toggle_pin'),
    path('toggle_archive/<int:note_id>/', views.toggle_archive, name='toggle_archive'),
    path('delete_note/<int:note_id>/', views.delete_note, name='delete_note'),
]