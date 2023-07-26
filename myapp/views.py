from django.shortcuts import render,redirect
from .models import Contact
from .models import User
from django.conf import settings
from django.core.mail import send_mail
import random


# Create your views here.
def index(request):
	return render(request,'index.html')

def contact(request):
	if request.method=='POST':
		Contact.objects.create(
			name=request.POST['name'],
			email=request.POST['email'],
			mobile=request.POST['mobile'],
			remarks=request.POST['remarks'],
			)
		msg="Contact Saved Successfully"
		contacts=Contact.objects.all().order_by("-id")[:3]
		return render(request,'contact.html',{'msg':msg,'contacts':contacts})
	else:
		contacts=Contact.objects.all().order_by("-id")[:3]
		return render(request,'contact.html',{'contacts':contacts})


def signup(request):
	if request.method=="POST":
		try:
			User.objects.get(email=request.POST['email'])
			msg="Email Alerady Existed"
			return render(request,"signup.html",{'msg':msg})
		except:
			if request.POST['password']==request.POST['cpassword']:
				User.objects.create(
					fname=request.POST['fname'],
					lname=request.POST['lname'],
					email=request.POST['email'],
					mobile=request.POST['mobile'],
					address=request.POST['address'],
					gender=request.POST['gender'],
					password=request.POST['password'],
					profile_pic=request.FILES['profile_pic']
					)
				msg="User Sign Up Successfully"
				return render(request,'signup.html',{'msg':msg})
			else:
				msg="Password and Confirm Password does not match."
				return render(request,'signup.html',{'msg':msg})
	else:
		return render(request,'signup.html')

	

def login(request):
	if request.method=="POST":
		try:
			user=User.objects.get(email=request.POST['email'])
			if user.password==request.POST['password']:
				request.session['email']=user.email
				request.session['fname']=user.fname
				request.session['profile_pic']=user.profile_pic.url
				return render(request,'index.html')
			else:
				msg="Incorrect Password"
				return render(request,'login.html',{'msg':msg})
		except:
			msg="Email Not Registerd"
			return render(request,'login.html',{'msg':msg})

	else:
		return render(request,'login.html')

def logout(request):
	try:
		del request.session['email']
		del request.session['fname']
		return render(request,'login.html')
	except:
		return render(request,'login.html')

def forgot_password(request):
	if request.method=='POST':
		try:
			user=User.objects.get(email=request.POST['email'])
			otp=random.randint(1000,9999)
			subject = 'OTP for forgot_password'
			message = 'Hello'+ user.fname + 'Your OTP for forgot_password is:'+str(otp)
			email_from = settings.EMAIL_HOST_USER
			recipient_list = [user.email, ]
			send_mail( subject, message, email_from, recipient_list )
			return render(request,'otp.html',{'email':user.email,'otp':otp})
		except Exception as e:
			print(e)
			msg='Email Not Registered'
			return render(request,'forgot-password.html',{'msg':msg})
	else:
		return render(request,'forgot-password.html')

def verify_otp(request):
	email=request.POST['email']
	otp=request.POST['otp']
	uotp=request.POST['uotp']
	if otp==uotp:
		return render(request,'new-password.html',{'email':email})
	else:
		msg='Incorrect Password'
		return render(request,'otp.html',{'msg':msg,'email':email,'otp':otp})

def new_password(request):
	email=request.POST['email']
	np=request.POST['new-password']
	cnp=request.POST['cnew-password']
	if np==cnp:
		user=User.objects.get(email=request.POST['email'])
		user.password=np
		user.save()
		msg='Password Update Successfully'
		return render(request,'login.html',{'msg':msg})
	else:
		msg='New password and Confirm new-password does not matched'
		return render(request,'new-password.html',{'msg':msg})

def change_password(request):
	if request.method=='POST':
		user=User.objects.get(email=request.session['email'])
		if user.password==request.POST['old-password']:
			if request.POST['new-password']==request.POST['cnew-password']:
				user.password=request.POST['new-password']
				user.save()
				return redirect('logout')
			else:
				msg='New password and Confirm new-password does not matched'
				return render(request,'change-password.html',{'msg':msg})
		else:
			msg='Old-password does not matched'
			return render(request,'change-password.html',{'msg':msg})
	else:
		return render(request,'change-password.html')


def profile(request):
	user=User.objects.get(email=request.session['email'])
	if request.method=='POST':
		user.fname=request.POST['fname']
		user.lname=request.POST['lname']
		user.email=request.POST['email']
		user.mobile=request.POST['mobile']
		user.address=request.POST['address']
		user.gender=request.POST['gender']
		try:
			user.profile_pic=request.FILES['profile_pic']
		except:
			pass
		user.save()
		request.session['profile_pic']=user.profile_pic.url
		msg='Profile Update Successfully'
		return render(request,'profile.html',{'user':user,'msg':msg})
	else:
		return render(request,'profile.html',{'user':user})

	
