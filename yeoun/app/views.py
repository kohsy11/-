from django.shortcuts import render, redirect
from .models import Todo, Comments
import datetime
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from .utils import upload_and_save
# Create your views here.
