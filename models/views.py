from django.shortcuts import render,redirect
from .models import Product
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate , login,logout
from django.contrib.auth.decorators import login_required
from .models import *
from django.core.paginator import Paginator
#-----------------------------------------------------------
#এটির কাজ হচ্ছে যদি ইউসার লগইন না হয় তাহলে একটি নিধারিত পেজ এ নেয়া যাবে 
# এবং যেই পেজ এর Function এর উপর দেয়া হবে সেই পেজ এ লগইন ছাড়া প্রবেশ করতে পারবে না
@login_required(login_url='login')
def resipy(request):
    # Create data -----------------------
    if request.method == "POST":
       
       data = request.POST
       title = data.get('title')
       description = data.get('description')
       price = data.get('price')
       imgs = request.FILES.get('imgs')

       Product.objects.create(
           title = title,
           description = description,
           price = price,
           imgs = imgs,
           )    
       return redirect('resipy')
    

# resipy list views codes ------------------------------------------
# এটি ব্যাকএন্ড থেকে ডাটা নিয়ে আসে অবজেক্ট আকারে
    queryest = Product.objects.all() 


   # Search resipy ------------------------------------------------------------
    if request.GET.get('search'):  #এর মাধ্যমে যা সার্চ করার জন্য লিখা হয়েছে তা এটী নিয়ে এসেছে
        queryest = queryest.filter(title__icontains = request.GET.get('search'))
   # search resipy end ---------------------------------------------------------

     
    context = {'resapy':queryest}  # queryest নামের অবজেক্ট টি নেয়া ডিকশেনারী আকারে তার কাছে স্টোরে করে
    return render(request, 'resipy.html',context) # মাধমে ডিকশেনারী টি HTML এ দেয়া দেয়া হয়েছে



# delete actions ------------------------------
@login_required(login_url='login')
def delete_resipy(request,id):
    queryset = Product.objects.get(id = id)
    queryset.delete()
    return redirect('resipy')

# Update actions ------------------------------
@login_required(login_url='login')
def update_resipy(request,id):
    queryset = Product.objects.get(id = id) #ডাটাবেস থেকে সব id এনে আমাদের দেয়া id র সাথে মেছ করানো হচ্ছে

    if request.method == "POST": #আমাদের দেয়া আপডেট রিকোয়েস্ট টি যদি পোস্ট আকারে আসে তাহলে এর ভিতরের সব কাজ করবে
        data = request.POST #পোস্ট আকারে যা আসবে তা স্টোরে করে রাখা হয়েছে

        #আমরা যা যা আপডেট করবো তা এখানে স্টোরে করে রাখা হবে
        title = data.get('title')
        description = data.get('description')
        price = data.get('price')
        imgs = request.FILES.get('imgs')

        #আমাদের স্টোরে করে রাখা আপডেট টি ডাটাবেস এর ডাটা কনভার্ট করে আমাদের দেয়া ডাটা সেভ করে দেয়া হবে
        queryset.title = title
        queryset.description = description
        queryset.price = price

        if imgs: #এখানে বলা হয়েছে যদি imgs ইনপুট যে কোনো আপডেট করি তাহলে imgs সোহো আপডেট হবে নাহলে আগের imgs টি এ থাকবে
            queryset.imgs = imgs
        queryset.save()
        return redirect('resipy')
    context = {'resipy':queryset}
    return render(request, 'update_resipy.html', context) #আপডেট এ ক্লিক করলেই এটি কাজ করবে
    

#এটি হলো লগইন করার function -----------------------------------------
def login_page(request):
    if request.method == "POST":
        #ইউসার এবং পাসওয়ার্ড টি ইনপুট থেকে নিয়ে আসা হয়েছে
        username = request.POST.get('username')
        password = request.POST.get('password')
      
        #এখানে বলা হয়েছে যদি এই username ডাটাবেস না থাকে
        #  তাহলে একটি error মেসেজ এর সাথে লগইন পেজ এ নেয়া যেও
        if not User.objects.filter(username = username).exists():
            messages.error(request, 'Invalid Username')
            return redirect('login')
        
        #জেহিত আমাদের Password টি ইনক্রিপ্ট করা authenticate এর মাধ্যমে ইউসার বের করতে হবে 
        # এর কাজ হলো ডাটা বের করা এখানে username and password বের করছে ডাটাবেস থেকে
        user = authenticate(username = username, password = password)

        #এখানে বলা হয়েছে যদি এই user  না থাকে তাহলে error এর সাথে লগইন এ নেয়া যেও  
        # নাহলে লগইন করাও লগইন authenticate এর মাধ্যমে
        if user is None:
            messages.error(request, 'Invalid Password')
            return redirect('login')
        else:
            login(request,user)
            return redirect('resipy')
    return render(request,'login.html')

#যদি Logout এ ক্লিক করে এই ফাঙ্কশন টি চালু হবে
def logout_page(request):
    logout(request)
    return redirect('login')



#এখানে ইউসার একাউন্ট তৈরী করার কোড রয়েছে-------------------
def register(request):
    #পোস্ট মেথড এর মাধ্যমে ইনপুট থেকে ডাটা আনা হয়েছে--------
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        #ইনপুট এ দেয়া ইউসার নাম টি আগে থেকে আছে কিনা তা চেক করা হচ্ছে
        user = User.objects.filter(username = username)

        #এখানে বলা হয়েছে যদি ইনপুট এ দেয়া ইউসার নাম টি আগে থেকে থাকে 
        # তাহলে আবার রেজিস্টার এ পাঠাও সাথে একটি এরর মেসেজ দেয়া দাও
        if user.exists():
            messages.info(request, 'Username already taken')
            return redirect('register')

        #এভাবে user তৈরী করা হয় ----------------------
        user = User.objects.create(
            first_name = first_name,
            last_name = last_name,
            username = username,
        )
        user.set_password(password) #user ডাটা কখনও ইনক্রিপ্ট হয় সেভ হয় না তাই এটির মাধ্যমে পাসওয়ার্ড টি ইনক্রিপ্ট করে সেভ করা হচ্ছে
        user.save()
        messages.info(request, 'account created Successfully')
        return redirect('register')

    return render(request,'register.html')

from django.db.models import Q,Sum
def set_students(request):
    queryset = Student.objects.all()
  
    #এটি সম্পূর্ণ সার্চ করার জন্য বানানো হয়েছে
    if request.GET.get('search'):
        search = request.GET.get('search')
        queryset =queryset.filter(
            #একহে বলা হয়েছে কোন কোন ডাটা গুলি icontains এর মাধবে আনতে হবে সার্চ করে
            Q(student_name__icontains = search) |
            Q(department__department__icontains = search) |
            Q(student_id__student_id__icontains = search) |
            Q(student_email__icontains = search) |
            Q(student_age__icontains = search)
        )

   # paginator ------------------------------
    paginator = Paginator(queryset,10) #এখানে বলা হয়েছে কয়টি অবজেক্ট বা ডাটা আসবে paginator এর মাধ্যমে
    page_number = request.GET.get("page" , 2) #শুরুতে কত নম্বর অবজেক্ট দেখাবে তা বলা হয়েছে
    page_obj = paginator.get_page(page_number)


    return render(request, 'report/students.html',{'queryset':page_obj})

from .seed import generate_report_card
#এটি স্টুডেন্ট এর মার্ক্স্ দেখার জন্য ----------------------
def see_marks(request , student_id):
    #এখানে student_id এর মাধ্যমে এই student_id কে ডাটাবেস থেকে বের করে আনা হয়েছে
    queryset = SubjectMarks.objects.filter(student__student_id__student_id = student_id)
    
    #এখানে স্টুডেন্ট এর টোটাল সাবজেক্ট এর মার্ক্স্ একত্রে করা হয়েছে Sum দেয়া
    total_marks = queryset.aggregate(total_marks = Sum('marks'))

    rank = ReportCard.objects.filter(student__student_id__student_id = student_id)
        
  
    return render(request , 'report/see_marks.html',{'queryset': queryset,'total_marks':total_marks,'rank': rank})
     
    