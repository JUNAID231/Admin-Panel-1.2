from django.contrib.auth import authenticate
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.core import serializers
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage


from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.status import HTTP_200_OK
#from rest_framework.authtoken.models import Token

from .models import User, Transaction, News, Admin, Chat, ChatUser
from .serializers import SignupSerializer, SigninSerializer, ListNewsSerializer, TransactionSerializer, CheckAmountSerializer, AddNewsSerializer, EditNewsSerializer, SearchAutherSerializer, AddAdminSerializer, ViewChatSerializer, CreateChatSerializer, ChatSignupSerializer

import string
from random import *
import datetime
import operator
import smtplib
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
import json
import hashlib






#--------------------------------
# Global Variables

NEWS_ID = '' # for News
USER_TYPE = ''  # for Admin Panel
USER_ID = '' # for Admin Panel
V1 = 'TEST'
V2 = ''


# Global Error
IS_ERROR = False
ERROR  = 'Error!'
CONTEXT = 'fields data are incorrect.'
FIELD = 'some fields are empty.'
EXIST = 'given email already registed.'
SESSION = 'your session has been expired.'

IS_SUCCESS = False
SUCCESS = 'Success!'
NEWUSER = 'new user has been successfuly added.'
DELETE_USER = 'user has been successfuly deleted.'
EDIT_USER = 'user has been successfuly edited.'
SUSPENDED = 'user has been successfuly suspended.'
ADD_NEWS = 'new news has been successfuly added.'
EDIT_NEWS = 'news has been successfuly edited.'
DELETE_NEWS = 'news has been successfuly deleted.'


#######################################################################################################
#                         User Registration API's                                                     
#######################################################################################################
#----------------------------------------------------------------------------------------------------
# 1: Signin User
#----------------------------------------------------------------------------------------------------

class SigninUser(APIView):

    queryset = User.objects.all()
    serializer_class = SigninSerializer

    
    def get (self, request):
        template_name  = "troyapi/signin.html"
        context = {}
        return render (request, template_name , context)

    def post(self, request):
        # Creating User Account
        emailaddress = request.POST.get('email')
        password = request.POST.get('password')
        
        if ( (emailaddress and emailaddress.strip()) and (password and password.strip()) ):
            #user = User.objects.get(emailaddress=emailaddress)
            user1 = User.objects.filter(emailaddress=emailaddress)
            # Email validation check
            if (not(user1)):
                print("------------------------------------------------------------")
                print("-            username and password are incorrect           -")
                print("------------------------------------------------------------")

                return Response ({'Error':' username and password are incorrect.'}, status=HTTP_200_OK)
            else:
                # Is user suspended or not
                user = User.objects.get(emailaddress=emailaddress)
                isSuspend = user.suspend
                if (isSuspend == "True"):
                    print ("----------------------------------------------")
                    print ("-           User has been suspended          -")
                    print ("----------------------------------------------")
                    return Response ({'Error': ' User has been suspended'}, status=HTTP_200_OK)
                else:
                   
                    mm = hashlib.md5()
                    mm.update(password.encode('utf-8'))
                    password = mm.hexdigest()
                    
                    print ('Password ', password)

                    userpassword = user.password
                    print ("Database Password :", userpassword)
                    if (userpassword == password):
                    
                        #------ Generating Token  ---------------------------
                        tokenLength = 30
                        tokenkey = ''.join(choice( str(datetime.datetime.today())+ string.ascii_uppercase+string.digits+string.ascii_lowercase ) for x in range(tokenLength))

                        #exitingToken = User.objects.all().values_list('signin_token') # Getting Token Colum
                        # Check: token is already exist or not
                        
                        #test = 's2452ct6624L9M-6-:0slaiJH2w2Xc9'
                    
                        matchToken = True
                        while (matchToken):
                            exist = User.objects.filter(signin_token=tokenkey) | User.objects.filter(signup_token=tokenkey)
                            if (exist):
                                print ("I found token.")
                                tokenkey = ''.join(choice( str(datetime.datetime.today())+ string.ascii_uppercase+string.digits+string.ascii_lowercase ) for x in range(tokenLength))
                            else:
                                print ("token does not found.")
                                user.signin_token = tokenkey
                                user.save()
                                expiry_date = datetime.datetime.today() + datetime.timedelta(days=31) # Setting Expiry Date
                                user.signin_timestamp = expiry_date
                                user.save()
                                matchToken = False
                
                        print("------------------------------------------------------------")
                        print("-            User has been successfully login.             -")
                        print("------------------------------------------------------------")
                        return Response ({'Token': user.signin_token}, status=HTTP_200_OK)
                    else:
                        print("------------------------------------------------------------")
                        print("-            username and password are incorrect           -")
                        print("------------------------------------------------------------")
                        return Response ({'Error':' username and password are incorrect.'}, status=HTTP_200_OK)
        else:
            print("------------------------------------------------------------")
            print("-            You are missing some fields.                  -")
            print("------------------------------------------------------------")
            return Response ({'Error':' You are missing some fields.'}, status=HTTP_200_OK )


#----------------------------------------------------------------------------------------------------
# 2: Signup User
#----------------------------------------------------------------------------------------------------
class SignupUser (APIView):
   
    queryset = User.objects.all()
    serializer_class = SignupSerializer

    def get (self, request):
        template_name  = "troyapi/signup.html"
        context = {}
        return render (request, template_name , context)

    def post(self, request):
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        emailaddress = request.POST.get('email')
        password = request.POST.get('password')

        if ( (firstname and firstname.strip()) and (lastname and lastname.strip()) and (emailaddress and emailaddress.strip()) and (password and password.strip()) ):
            #unvalidEmail = Signup.objects.filter(email=email)
            useremail = User.objects.all().filter(emailaddress=emailaddress)
            
            if (not(useremail)):
                print("------------------------------------------------------------")
                print("-            User has been successfully created.           -")
                print("------------------------------------------------------------")
                mm = hashlib.md5()
                mm.update(password.encode('utf-8'))
                password = mm.hexdigest()
            
                newuser = User(firstname=firstname, lastname=lastname, emailaddress=emailaddress, password=password) # Insert User to database
                newuser.save()
                
                #------------- Generating Token  -----------------------------
                tokenLength = 30
                tokenkey = ''.join(choice( str(datetime.datetime.today()) + string.ascii_uppercase+string.digits+string.ascii_lowercase ) for x in range(tokenLength))
                print ("Token Key : ",tokenkey)

                matchToken = True
                while (matchToken):
                    exist = User.objects.filter(signin_token=tokenkey) | User.objects.filter(signup_token=tokenkey)
                    if (exist):
                        print ("I found token.")
                        tokenkey = ''.join(choice( str(datetime.datetime.today())+ string.ascii_uppercase+string.digits+string.ascii_lowercase ) for x in range(tokenLength))
                        
                    else:
                        print ("token does not found.")
                        newuser.signup_token = tokenkey
                        newuser.save()
                        expiry_date = datetime.datetime.today() + datetime.timedelta(days=31) # Setting Expiry Date
                        newuser.signup_timestamp = expiry_date
                        newuser.save()
                        matchToken = False

                last_user = User.objects.all().last() # getting last user details
                serializer = SignupSerializer(last_user, many=False) # Convert Queryset into json formate
                # dont use lat {email firstname lastname token }           
                return Response ( serializer.data , status=HTTP_200_OK)
            else:
                print("------------------------------------------------------------")
                print("-            This email is already registed.               -")
                print("------------------------------------------------------------")
                return Response ({'Error':' This email is already registed.'}, status=HTTP_200_OK)
        else:
            print("------------------------------------------------------------")
            print("-            Fields are empty                   			  -")
            print("------------------------------------------------------------")
            return Response ({'Error':' You are missing some fields.'}, status=HTTP_200_OK)



#######################################################################################################
#                          Send/Receive Funds via email: API's
#######################################################################################################
#---------------------------------------------------------------------------------------------------
# 1: Transfer Funds Via Email
#---------------------------------------------------------------------------------------------------
class TransferFund(APIView):
    # transfer = Transaction.objects.all()
    # serializer_class = TransactionSerializer

    # def get (self, request):
    #     template_name  = "registration/form.html"
    #     context = {}
    #     return render (request, template_name , context)

    def post(self, request):

        user_token = request.POST.get('token') # who want to do the transaction

        to_emailaddress = request.POST.get('email')
        from_emailaddress = request.POST.get('from_email')
        amount = request.POST.get('amount')
        from_walletID = request.POST.get('from_walletID')

        if( (to_emailaddress and to_emailaddress.strip()) and (amount and amount.strip()) and (from_walletID and from_walletID.strip()) and (user_token and user_token.strip()) ):
            
            # Check: User Token
            user_tok = User.objects.filter(emailaddress=from_emailaddress, signup_token=user_token) | User.objects.filter(emailaddress=from_emailaddress, signin_token=user_token)
            if (not(user_tok)):
                print ("---------------------------------")
                print ("-    Token does not Found.      -")
                print ("---------------------------------")
                return Response ({'Error': ' user token does not exist.'}, status=HTTP_200_OK)
            else:
                #Check: Is current suser is suspend or not
                # print ("Is current user has been suspend??")
                # user_sus = User.objects.get(emailaddress=from_emailaddress, signup_token=user_token)
                
                # isSuspend = user_sus.suspend
                # print ("isSuspend: ",isSuspend)
                # if (isSuspend == "True"):
                #     print("--------------------------------------------------------")
                #     print ("-          User token has been suspended              -")
                #     print("--------------------------------------------------------")
                #     return Response ({'Error': ' User has been suspended.'}, status=HTTP_200_OK)
                # else:
                
                to_email = User.objects.order_by('user_id').filter(emailaddress=to_emailaddress )
                if (not(to_email)):
                    print ("Given email address is not exist in our database.")
                    # Given email address does not exist in our database
                    # Notification to recevier: Download our application to get this amount.

                    to_id = 000
                    codeLength = 10
                    code_key = ''.join(choice(string.ascii_uppercase+string.digits+string.ascii_lowercase) for x in range(codeLength))
                    StoreData(self, from_walletID, to_emailaddress, to_id, amount, code_key) # Store data to database
                    EmailSend(self) # Send Email to recevier

                    return Response({'Detail': ' Given email address is not exist in our database.'}, status=HTTP_200_OK)
                else:
                    print ("Email found.")
                    # Given email address exist in our database 
                    # Notification to recevier: Confirm this transaction.
                    # Store data to the database server
                
                    # Generating Transaction Code
                    codeLength = 10
                    code_key = ''.join(choice(string.ascii_uppercase+string.digits+string.ascii_lowercase) for x in range(codeLength))
                
                    to_walletID = 111

                    StoreData(self,from_walletID, to_emailaddress, to_walletID, amount, code_key) # Store data to the server
                    return Response ({'Detail ': ' Transaction successfuly sended.'}, status=HTTP_200_OK)

        else:
            print ("--------------------------------------------------------------------------")
            print ("-                         Error: Fields are empty                        -")
            print ("--------------------------------------------------------------------------")
            return Response ({'Error': ' You are missing some fields.'}, status=HTTP_200_OK)

    
# Store data to the server 
def StoreData(self,from_walletID, to_email, to_walletID, amount, code ):
    transfered = Transaction( from_walletID=from_walletID, to_walletID=to_walletID, to_emailaddress=to_email, amount=amount, transaction_code=code )
    transfered.save()
    return Response ({'Detail': ' Transaction has been sended successfuly.'}, status=HTTP_200_OK)

# Send email to the fund recevier
def EmailSend(self):
    #print ("Email function")
    body = "download our app to get this transaction. click"
    _to = 'thebooster786@gmail.com'
    _from = 'thebooster786@gmail.com'
    _password = 'junaid786'

    connection = smtplib.SMTP('smtp.gmail.com',587)
    connection.ehlo()
    connection.starttls()
    connection.login( _from, _password)
    connection.sendmail( _from, _to, body)
    #connection.send()
    connection.quit()


#-----------------------------------------------------------------------------------------------------
# 2: Check your all email transaction amounts and Recevie them                  
#-----------------------------------------------------------------------------------------------------
class Amount(APIView):
    
    queryset = Transaction.objects.all()
    serializer_class = CheckAmountSerializer

    def get(self, request):
        template_name  = "troyapi/recevieFunds.html"
        context = {}
        return render (request, template_name , context)
    
    def post(self, request):
        myemail = request.POST.get('email') # who want to see his email transaction
        user_token = request.POST.get('token') # who want to see his email transaction
        #transaction_code = request.POST.get('code')

        if ( (myemail and myemail.strip()) and (user_token and user_token.strip()) ):
            # check: user is registed or not 
            user_tok = User.objects.filter(emailaddress=myemail, signup_token=user_token) | User.objects.filter(emailaddress=myemail, signin_token=user_token)
            if (not (user_tok)):
                print ('--------------------------------------')
                print ('-  incorrect email and token.        -')
                print ('--------------------------------------')
                return Response({'Error': ' incorrect email and token.'}, status=HTTP_200_OK )
            else:
                print ('--------------------------------------')
                print ('-  valid email and token.            -')
                print ('--------------------------------------')

                user = Transaction.objects.filter(to_emailaddress=myemail)
                #print ("User ", len(user))
                #exitingToken = Transfer.objects.all().values_list('signup_token')
                if (not (user)):
                    print ("-------------------------------------")
                    print ("-    Email does not exist           -")
                    print ("-------------------------------------")
                    return Response ({'Error': ' Email does not exist.'}, status=HTTP_200_OK)
                else:
                    # Return all the token sent via email which are not accepted yet.
                    # user = Transfer.objects.get(to_emailaddress=myemail)
                    # print ("Bobi : ", user.transaction_code)

                    print ("length : ", len(user))
                    i=0
                    while (i < len(user)):
                        print ("Object",user[i])
                        data = str(user[i])
                        print ("Data",data)
                        if (data == "Pending"):
                            print ("Token at this email address: ")
                            #return Response ({'Details':' Status'}, status=HTTP_200_OK)
                        else:
                            print ("No Pending")
                            #return Response ({'Error':' No pending transactions.'}, status= HTTP_200_OK)
                        i+=1

                    hep = Transaction.objects.filter(to_emailaddress=myemail) 
                    serializer = CheckAmountSerializer(hep, many=True) # Convert Queryset to json
                    return Response (serializer.data, status= HTTP_200_OK)
            
        else:
            print ("Fields are empty.")
            return Response ({'Error': ' You are missing some fields.'}, status=HTTP_200_OK)

    
#-----------------------------------------------------------------------------------------------------
# 3: Recevied Token and update record                  
#-----------------------------------------------------------------------------------------------------
class ConfirmStatus(APIView):
    
    queryset = Transaction.objects.all()
    serializer_class = CheckAmountSerializer

    def get(self, request):
        template_name  = "troyapi/recevieFunds.html"
        context = {}
        return render (request, template_name , context)
    
    def post(self, request):
        user_token = request.POST.get('token') # who want to confirm his transaction

        myemail = request.POST.get('email') # who want to confirm his transaction
        transaction_code = request.POST.get('code') # who want to confirm his transaction
        

        if ( (myemail and myemail.strip()) and (transaction_code and transaction_code.strip()) and (user_token and user_token.strip()) ):
            
            # check: user has downloaded our app
            # check: user is registed or not
            user_tok = User.objects.filter(emailaddress=myemail, signup_token=user_token) | User.objects.filter(emailaddress=myemail, signin_token=user_token)
            if (not (user_tok)):
                print ('--------------------------------------')
                print ('- incorrect user email, token or code.')
                print ('--------------------------------------')
                return Response({'Error': ' incorrect email and token.'}, status=HTTP_200_OK)
            else:
                print ('--------------------------------------')
                print ('-  valid email and token.            -')
                print ('--------------------------------------')

                # check: User has any transaction
                user = Transaction.objects.filter(to_emailaddress=myemail, transaction_code=transaction_code)
                if (not(user)):
                    print("--------------------------------------------")
                    print("-      incorrect user email and code       -")
                    print("--------------------------------------------")
                    return Response ({'Error': ' incorrect user email and code.'}, status=HTTP_200_OK)
                else:
                    # Check transaction code and update its status
                    code = Transaction.objects.get(transaction_code=transaction_code)
                    if (not(code)):
                        print ("--------------------------------------")
                        print ("-      Code does not matach          -")
                        print ("--------------------------------------")
                        return Response ({'Error': 'Code does not matach'}, status=HTTP_200_OK)
                    else:
                        status = code.status
                        if (status =='Pending'):
                            # run smart contract code
                            # update the recored  
                            code.status = 'Success'
                            code.save()
                            print('Send notification that you have successfuly recevied token.')
                            return Response ({'Detail': ' Send notification that you have successfuly recevied token'}, status=HTTP_200_OK)
                        else:
                            print ('There is no pending transaction.')
                            return Response ({'Error': ' There is no pending transaction.'}, status=HTTP_200_OK)

        else:
            print ("Fields are empty.")
            return Response ({'Error': ' fields are empty.'}, status=HTTP_200_OK) 


######################################################################################################
#                           News API's
######################################################################################################
#------------------------------------------------------------------------------------------------------
# 1: Add News
#------------------------------------------------------------------------------------------------------
#viewsets.ModelViewSet
class AddNews(APIView):
    # queryset = News.objects.all()
    # serializer_class = AddNewsSerializer
    template_name  = "troyapi/admin-add-news/add-news/base_layout.html"

    def get(self, request):
        
        context = {}
        return render (request, self.template_name , context)

    def post(self,request):
        # admin_token = request.POST.get('token') # admin token

        # adding new news fields
        category = request.POST.get('category')
        title = request.POST.get('title')
        short_description = request.POST.get('short-description')
        long_description = request.POST.get('long-description')
        photo = request.POST.get('photo')
        auther = request.POST.get('auther')

        global IS_SUCCESS, SUCCESS, ADD_NEWS, ERROR, FIELD, IS_ERROR

        if ( (category and category.strip()) and (title and title.strip()) and (short_description and short_description.strip()) and (long_description and long_description.strip()) and  (auther and auther.strip()) ):
            
            # Check: Admin Token
            # admin_token = Admin.objects.filter(token=admin_token)
            # if ( not(admin_token) ):
            #     print ("--------------------------------------")
            #     print ("-          Invalid admin token       -")
            #     print ("--------------------------------------")
            #     return Response ({'Error': ' Invalid admin token.'}, status=HTTP_200_OK)
            # else:   

            newNews = News(category=category, title=title, short_description=short_description, long_description=long_description, auther=auther, photo=photo )
            newNews.save()
            newNews.timestamp = datetime.datetime.today()
            newNews.save()
            print("------------------------------------------------------------------------")
            print("-              New news has been added                                 -")
            print("------------------------------------------------------------------------")
            # Converting object into json serializer
            
            IS_SUCCESS = True
            context = { 'SUCCESS': SUCCESS, 'CONTEXT': ADD_NEWS, 'IS_SUCCESS': IS_SUCCESS }
            return render (request, self.template_name , context)
           
        else:
            print("------------------------------------------------------------------------")
            print("-               Some fields are empty                                  -")
            print("------------------------------------------------------------------------")
            #return Response({'Error':' fields are empty'}, status=HTTP_200_OK)
            
            IS_ERROR = True
            context = { 'ERROR': ERROR, 'CONTEXT': FIELD, 'IS_ERROR': IS_ERROR }
            return render (request, self.template_name , context)

#------------------------------------------------------------------------------------------------------
# 2: Search Auther
#------------------------------------------------------------------------------------------------------

# class SearchAuther(APIView):

#     queryset = News.objects.all()
#     serializer_class = SearchAutherSerializer

#     def get(self, request):
#         template_name  = "registration/newsid.html"
#         context = {}
#         return render (request, template_name , context)

#     edit_auther = ''

#     def post(self, request):
#         auther = request.POST.get('auther')
#         print ("Auther : ", auther)

#         if ( auther and auther.strip() ):
#             auther = News.objects.get(auther_id=auther)
#             edit_auther = auther.auther_id
#             globalFunc(edit_auther)
#             if (not(auther)):
#                 print("------------------------------------------------------------------------")
#                 print("-              Not Exist                                               -")
#                 print("------------------------------------------------------------------------")
#                 #return Response ({'Error':' ID does not exist.'}, status=HTTP_200_OK)
#             else:
#                 print("------------------------------------------------------------------------")
#                 print("-              Auther Exist                                            -")
#                 print("------------------------------------------------------------------------")
#                 re = redirect ('edit')
#                 return re
#         else:
#             print("------------------------------------------------------------------------")
#             print("-             Fields are empty                                         -")
#             print("------------------------------------------------------------------------")
#             return Response({'Error': ' Fields are empty.'}, status=HTTP_200_OK)

# #----  Assing Auther id to global veriable -------------
# def globalFunc(edit_auther):
#     global global_id
#     global_id = edit_auther
#     print("global 1 : ",global_id)

#---------------------------------------------------------------------------------------------
# 3: Edit News
#---------------------------------------------------------------------------------------------

def EditNews(request, news_id):
    # print (news_id)
    # global NEWS_ID
    # NEWS_ID = news_id
    red = redirect ('redirect-edit-news')
    return red

def CallMe( request, news_id ):
    print (news_id)
    global NEWS_ID
    NEWS_ID = news_id
    red = redirect ('redirect-edit-news')
    return red

class RedirectEditNews(APIView):

    template_name  = "troyapi/admin-edit-news/edit-news/base_layout_redirect.html"
    def get (self, request):
        global NEWS_ID
        old_news = News.objects.get(news_id = NEWS_ID)

        old_category = old_news.category
        old_title = old_news.title
        old_short_description = old_news.short_description
        old_long_description = old_news.long_description
        old_auther = old_news.auther

        context = {'old_category': old_category, 'old_title': old_title, 'old_short_description': old_short_description, 'old_long_description': old_long_description, 'old_auther': old_auther }
        return render (request, self.template_name , context)

    def post(self, request):
        
        category = request.POST.get('category') # update category for news id
        title = request.POST.get('title') #  update title for news id
        short_description = request.POST.get('short_description') # update short description for news id
        long_description = request.POST.get('long_description') # update long description for news id
        auther = request.POST.get('auther') # update auther for news id
        photo = request.POST.get('photo') # update photo for news id

        global ERROR, CONTEXT, IS_ERROR, EDIT_NEWS, FIELD, SESSION

        if ((category and category.strip()) and (title and title.strip()) and (short_description and short_description.strip()) and (long_description and long_description.strip()) and (auther and auther.strip()) ):
            
            global NEWS_ID
            news_id =  NEWS_ID
            # Check: SESSION
            Checkif = False
            if ( Checkif == True ):
                print ("-----------------------------------------")
                print ("-      Your Session has been expired    -")
                print ("-----------------------------------------")
                IS_ERROR = True
                context = { 'ERROR': ERROR, 'CONTEXT': SESSION, 'IS_ERROR': IS_ERROR }
                return render (request, self.template_name , context)
                #return Response ({'Error': ' Invalid fields address.'}, status= HTTP_200_OK)
            else:
                print ("-----------------------------------------")
                print ("-      upating news fields              -")
                print ("-----------------------------------------")
                print ("News id:", news_id)
                update_news = News.objects.get(news_id=news_id)

                update_news.category = category
                update_news.save()
                update_news.title = title
                update_news.save()
                update_news.short_description = short_description
                update_news.save()
                update_news.long_description = long_description
                update_news.save()
                update_news.auther = auther
                update_news.save()
                update_news.timestamp = datetime.datetime.today()
                update_news.save()
                
                IS_SUCCESS = True
                context = { 'SUCCESS': SUCCESS, 'CONTEXT': EDIT_NEWS, 'IS_SUCCESS': IS_SUCCESS }
                return render (request, self.template_name , context)
                #return Response ({'Success': ' News updated'}, status= HTTP_200_OK)
        else:
            print ("-----------------------------------------")
            print ("-         Fields are empty              -")
            print ("-----------------------------------------")
            IS_ERROR = True
            context = { 'ERROR': ERROR, 'CONTEXT': FIELD, 'IS_ERROR': IS_ERROR }
            return render (request, self.template_name , context)
            #return Response ({'Error': ' Fields are empty.'}, status=HTTP_200_OK)
        
#------------------------------------------------------------------------------------------
# 4: Delete News
#------------------------------------------------------------------------------------------
#viewsets.ModelViewSet

def Remove(request, delete_id):

    news_id = delete_id  # news id that will be going to be deleted
    delete_news = News.objects.filter(news_id=news_id)
    delete_news.delete()
    red = redirect ('list-news-interface')
    return red

class DeleteNews(APIView):
    def get (self,request):
        return HttpResponse ("NO")
#-----------------------------------------------------------------------------------------------------
# 5: List News  API's               
#-----------------------------------------------------------------------------------------------------
class ListNews (APIView):

    def get(self,request):
        news = News.objects.all()    
        serializers = ListNewsSerializer(news, many=True)
        return Response (serializers.data, status=HTTP_200_OK)
       
#-----------------------------------------------------------------------------------------------------
# 5: Admin List News Interface               
#-----------------------------------------------------------------------------------------------------

class ListNewsIneterface (APIView):

    def get(self,request):
        template_name  = "troyapi/list-news/news/base_layout.html"
        news = News.objects.all()
        arg = {'news': news}
        return render (request, template_name , arg )

#######################################################################################################
#                               Admin Panel API's
#######################################################################################################
#-----------------------------------------------------------------------------------------------------
# 1: Signin Admin                 
#-----------------------------------------------------------------------------------------------------
class SigninAdmin(APIView):

    template_name  = "troyapi/admin-login/login/index.html"
    
    queryset = User.objects.all()
    serializer_class = SigninSerializer
    
    def get (self, request):
        context = {}
        return render (request, self.template_name , context)

    def post(self, request):
        # Creating User Account
        emailaddress = request.POST.get('username')
        password = request.POST.get('pass')

        global ERROR, CONTEXT, IS_ERROR, SUSPENDED, FIELD

        if ( (emailaddress and emailaddress.strip()) and (password and password.strip()) ):
            admin = Admin.objects.filter(emailaddress=emailaddress)
            # Email validation check
            if (not(admin)):
                print("------------------------------------------------------------")
                print("-     Error! username and password are incorrect           -")
                print("------------------------------------------------------------")
                
                IS_ERROR = True
                context = { 'ERROR': ERROR, 'CONTEXT': CONTEXT, 'IS_ERROR': IS_ERROR }
                return render (request, self.template_name , context)
                #return Response ({'Error':' username and password are incorrect.'}, status=HTTP_200_OK)
            else:
                # Password validation
                admin = Admin.objects.get(emailaddress=emailaddress)
                userpassword = admin.password
                if (userpassword == password):
                    
                    isSuspend = admin.suspend
                    if (isSuspend == "True"):
                        print ("----------------------------------------------")
                        print ("-           User has been suspended          -")
                        print ("----------------------------------------------")
                      
                        IS_ERROR = True
                        context = { 'ERROR': ERROR, 'CONTEXT': SUSPENDED, 'IS_ERROR': IS_ERROR }
                        return render (request, self.template_name , context)
                    else:
                        print("------------------------------------------------------------")
                        print("-            User has been successfully login.             -")
                        print("------------------------------------------------------------")
                        
                        userid = admin.admin_id
                        print ("User ID : ", userid)
                        request.session['userid'] = userid
                        ses = request.session['userid']
                        print ("SESSION USER ID ",ses)
                        
                        IS_ERROR = False
                        
                        red = redirect ('create-user')
                        return red
                        # template_name  = "registration/admin-create-user/create-user/index.html"
                        # context = {}
                        # return render (request, template_name , context)
                else:
                    print("------------------------------------------------------------")
                    print("-     Error! username and password are incorrect           -")
                    print("------------------------------------------------------------")
                        
                    IS_ERROR = True
                    context = { 'ERROR': ERROR, 'CONTEXT': CONTEXT, 'IS_ERROR': IS_ERROR }
                    return render (request, self.template_name , context)

        else:
            print("------------------------------------------------------------")
            print("-     Error! You are missing some fields.                  -")
            print("------------------------------------------------------------")
    
            IS_ERROR = True
            context = { 'ERROR': ERROR, 'CONTEXT': FIELD, 'IS_ERROR': IS_ERROR }
            return render (request, self.template_name , context)
            #return Response ({'Error':' You are missing some fields.'}, status=HTTP_200_OK )


#-----------------------------------------------------------------------------------------------------
# 3: Signout Admin                 
#-----------------------------------------------------------------------------------------------------

class SignoutAdmin(APIView):

    def get (self, request):
        del request.session['userid']
        print ("Session has been deleted.")
        template_name  = "troyapi/admin-login/login/index.html"
        context = {}
        return render (request, template_name , context)


#-----------------------------------------------------------------------------------------------------
# 3: Create Admin                 
#-----------------------------------------------------------------------------------------------------
class CreateAdmin (APIView):
    template_name  = "troyapi/admin-create-user/create-user/base_layout.html"
    
    def get (self, request):    
        context = {}
        return render (request, self.template_name , context)

    def post (self, request):
        #admin_token = request.POST.get('token') # Admin token 
        
        # Create new admin user fields
        firstname = request.POST.get('first_name') # admin user first name
        lastname = request.POST.get('last_name') # admin user last name
        emailaddress = request.POST.get('email') # admin user email address
        password = request.POST.get('password') # admin user password

        global ERROR, SESSION, IS_ERROR, SUCCESS, NEWUSER, IS_SUCCESS, EXIST, FIELD

        if ( not request.session.has_key('userid') ):
            print ("Error : Your Session has been expired.")
            
            IS_ERROR = True
            context = { 'ERROR': ERROR, 'CONTEXT': SESSION, 'IS_ERROR': IS_ERROR }
            return render (request, self.template_name , context)
        else:

            if ( (firstname and firstname.strip()) and (lastname and lastname.strip()) and (emailaddress and emailaddress.strip()) and (password and password.strip()) ):
                
                # Check: Given email already registed or not
                # Check: Is it valide admin or not
                # admintoken = Admin.objects.filter(token=admin_token)
                newadmin = Admin.objects.filter(emailaddress=emailaddress)
                if ( not(newadmin) ):
                    print ("---------------------------------------------------------")
                    print ("-    New Admin has been created                         -")
                    print ("---------------------------------------------------------")
                    
                    admin = Admin(firstname=firstname, lastname=lastname, emailaddress=emailaddress, password=password)
                    admin.save()                  
                    expire_date = datetime.datetime.today() + datetime.timedelta(days=31)
                    admin.timestamp = expire_date
                    admin.save()

                    IS_SUCCESS = True
                    IS_ERROR = False
                    context = { 'SUCCESS': SUCCESS, 'CONTEXT': NEWUSER, 'IS_SUCCESS': IS_SUCCESS }
                    return render (request, self.template_name , context)
                    #return Response({'Success': ' Admin has been addes.'}, status=HTTP_200_OK)
                    
                else:
                    print ("---------------------------------------------------------")
                    print ("-     Given email address already exist in database     -")
                    print ("---------------------------------------------------------")
            
                    IS_ERROR = True
                    context = { 'ERROR': ERROR, 'CONTEXT': EXIST, 'IS_ERROR': IS_ERROR }
                    return render (request, self.template_name , context)
                    #return Response({'Error':' Given email address already exist in database'}, status=HTTP_200_OK)
                
            else:
                print("-----------------------------------------------------------")
                print("-                Error: Fields are empty                  -")
                print("-----------------------------------------------------------")

                IS_ERROR = True
                context = { 'ERROR': ERROR, 'CONTEXT': FIELD, 'IS_ERROR': IS_ERROR }
                return render (request, self.template_name , context)
                #return Response({'Error': ' Fields are empty.'}, status=HTTP_200_OK)

#-----------------------------------------------------------------------------------------------------
# 2: Delete Admin                                                                                      
#-----------------------------------------------------------------------------------------------------
class DeleteAdmin(APIView):

    template_name  = "troyapi/admin-delete-user/delete-user/base_layout.html"

    def get(self, request):
        context = {}
        return render (request, self.template_name , context)

    def post (self, request):
        #emailaddress = request.POST.get('email') 
        #admin_token = request.POST.get('token') # admin token, who want to perfom action
        user_id = request.POST.get('userid') # 
        user_type = request.POST.get('subject')
        
        global ERROR, SESSION, IS_ERROR, CONTEXT, SUCCESS, DELETE_USER, IS_SUCCESS, FIELD

        if ( not request.session.has_key('userid') ):
            print ("Error : Your Session has been expired.")
            
            IS_ERROR = True
            context = { 'ERROR': ERROR, 'CONTEXT': SESSION, 'IS_ERROR': IS_ERROR }
            return render (request, self.template_name , context)
        else:

            if ( (user_id and user_id.strip()) and (user_type and user_type.strip() ) ):
                # Check: do you want delete admin or normal user?
                if (user_type == 'Admin'):
                    # Deleteing Admin User
                    delete_admin = Admin.objects.filter(admin_id=user_id )
                    if (not(delete_admin)):
                        print ("-------------------------------------------------------")
                        print ("    Error! Admin does not exist in our database.       ")
                        print ("-------------------------------------------------------")

                        IS_ERROR = True
                        context = { 'ERROR': ERROR, 'CONTEXT': CONTEXT, 'IS_ERROR': IS_ERROR }
                        return render (request, self.template_name , context)
                        #return Response({'Error ': 'Admin does not exist in our database.'}, status=HTTP_200_OK)
                    else:
                        print ("-------------------------------------------------------")
                        print ("    Success! Admin has been deleted in our database.   ")
                        print ("-------------------------------------------------------")
                        delete_admin.delete()

                        IS_SUCCESS = True
                        context = { 'SUCCESS': SUCCESS, 'CONTEXT': DELETE_USER, 'IS_SUCCESS': IS_SUCCESS }
                        return render (request, self.template_name , context)
                        #return Response({'Success ': 'Admin has been deleted in our database.'}, status=HTTP_200_OK)

                elif ( user_type == 'User' ):
                    # Deleting Normal User
                    delete_user = User.objects.filter(user_id=user_id )
                    if (not(delete_user)):
                        print ("-------------------------------------------------------")
                        print ("    Error! User does not exist in our database.        ")
                        print ("-------------------------------------------------------")
                        
                        IS_ERROR = True
                        context = { 'ERROR': ERROR, 'CONTEXT': CONTEXT, 'IS_ERROR': IS_ERROR }
                        return render (request, self.template_name , context)
                        #return Response({'Error ': 'User does not exist in our database.'}, status=HTTP_200_OK)
                    else:
                        print ("-------------------------------------------------------")
                        print ("    Success! User has been deleted in our database.   ")
                        print ("-------------------------------------------------------")
                        delete_user.delete()
                        
                        IS_SUCCESS = True
                        context = { 'SUCCESS': SUCCESS, 'CONTEXT': DELETE_USER, 'IS_SUCCESS': IS_SUCCESS }
                        return render (request, self.template_name , context)
                        #return Response({'Success ': 'User has been deleted in our database.'}, status=HTTP_200_OK)
                        
                else:
                    print ("Not a valid user type.")
                    return Response ({'Error ': ' Invalid User Type.'}, status=HTTP_200_OK)

            else: 
                print("--------------------------------")
                print("-      Field are empty         -")
                print("--------------------------------")
                
                IS_ERROR = True
                context = { 'ERROR': ERROR, 'CONTEXT': FIELD, 'IS_ERROR': IS_ERROR }
                return render (request, self.template_name , context)
               # return Response ({'Error': ' Field are empty.'}, status=HTTP_200_OK)


#-----------------------------------------------------------------------------------------------------
# 3: Edit Admin                 
#-----------------------------------------------------------------------------------------------------
class EditUser(APIView):
    def get (self, request):
        return HttpResponse("Hell0")


def EditUserW (request, user_type, user_id):

    global USER_TYPE, USER_ID
    USER_TYPE = user_type
    USER_ID = user_id
    red  = redirect ("redirect-edit-user")
    return red
    

class RedirectEditUser(APIView):

    template_name  = "troyapi/admin-edit-user/edit-user/base_layout_redirect.html"

    def get(self, request):

        global USER_TYPE, USER_ID
        user_type = USER_TYPE
        user_id = USER_ID
        if (user_type == 'User'):
            user_data = User.objects.get (user_id=user_id)
            old_firstname = user_data.firstname
            old_lastname = user_data.lastname
            old_email = user_data.emailaddress
            old_password = user_data.password
        elif (user_type == 'Admin'):
            admin_data = Admin.objects.get (admin_id=user_id)
            old_firstname = admin_data.firstname
            old_lastname = admin_data.lastname
            old_email = admin_data.emailaddress
            old_password = admin_data.password


        context = {'old_firstname': old_firstname , 'old_lastname': old_lastname, 'old_email': old_email, 'old_password': old_password }
        return render (request, self.template_name , context)

    def post(self, request):
        
        firstname = request.POST.get('first_name') # update first name of user id
        lastname = request.POST.get('last_name') # update last name of user id
        emailaddress = request.POST.get('email') # update email address of user id
        password = request.POST.get('password') # update password of user id

        global ERROR, CONTEXT, IS_ERROR, SUCCESS, IS_SUCCESS, EDIT_USER

        if ( (firstname and firstname.strip()) and (lastname and lastname.strip()) and (emailaddress and emailaddress.strip()) and (password and password.strip()) ):
            global USER_TYPE, USER_ID
            user_type = USER_TYPE
            user_id = USER_ID

            user_email  = Admin.objects.filter( emailaddress=emailaddress )
            if ( user_email ):
                print("--------------------------------------")
                print("- Error! incorrect admin token       -")
                print("--------------------------------------")
                IS_ERROR = True
                context = { 'ERROR': ERROR, 'CONTEXT': CONTEXT, 'IS_ERROR': IS_ERROR }
                return render (request, self.template_name , context)
                #return Response ({'Error': ' Incorrect admin token.'}, status=HTTP_200_OK)
            else:
                print("--------------------------------")
                print("-         Edit User            -")
                print("--------------------------------")
                if (user_type == 'Admin'):
                    # Edit Admin User
                    edit_admin = Admin.objects.get(admin_id=user_id )
                    edit_admin.firstname = firstname
                    edit_admin.save()
                    edit_admin.lastname = lastname
                    edit_admin.save()
                    edit_admin.emailaddress = emailaddress
                    edit_admin.save()
                    # Converting Password into MD file
                    mm = hashlib.md5()
                    mm.update(password.encode('utf-8'))
                    password = mm.hexdigest()
                    edit_admin.password = password
                    edit_admin.save()
                    print("------------------------------------------")
                    print("-    Success! Admin has been edited      -")
                    print("------------------------------------------")
                    IS_SUCCESS = True
                    IS_ERROR = False
                    context = { 'SUCCESS': SUCCESS, 'CONTEXT': EDIT_USER, 'IS_SUCCESS': IS_SUCCESS }
                    return render (request, self.template_name , context)
                    #return Response ({'Success': ' User has been edited.'}, status=HTTP_200_OK)
                    
                elif ( user_type == 'User' ):
                    # Edit Normal User
                    edit_user = User.objects.get(user_id=user_id )
                    edit_user.firstname = firstname
                    edit_user.save()
                    edit_user.lastname = lastname
                    edit_user.save()
                    edit_user.emailaddress = emailaddress
                    edit_user.save()
                    edit_user.password = password
                    edit_user.save()
                    print("------------------------------------------")
                    print("-    Success! User has been edited       -")
                    print("------------------------------------------")
                    IS_SUCCESS = True
                    IS_ERROR = False
                    context = { 'SUCCESS': SUCCESS, 'CONTEXT': EDIT_USER, 'IS_SUCCESS': IS_SUCCESS }
                    return render (request, self.template_name , context)
                    #return Response ({'Success': ' User has been edited.'}, status=HTTP_200_OK)
                else:
                    print ("Invalid user type.")
                    return Response ({'Error': ' invalid user type.'}, status=HTTP_200_OK)
        else:
            print("--------------------------------")
            print("-      Fields are empty        -")
            print("--------------------------------")
            IS_ERROR = True
            context = { 'ERROR': ERROR, 'CONTEXT': FIELD, 'IS_ERROR': IS_ERROR }
            return render (request, self.template_name , context)
            #return Response ({'Error': ' Fields are empty.'}, status=HTTP_200_OK)


#-----------------------------------------------------------------------------------------------------
# 4 : Suspend User                 
#-----------------------------------------------------------------------------------------------------
class Suspend(APIView):
    
    template_name  = "troyapi/admin-edit-user/edit-user/base_layout_suspend.html"
    
    def get (self, request):
        context = {}
        return render (request, self.template_name , context)

    def post (self, request):
        #admin_token = request.POST.get('admintoken') # who want to suspend user
        user_id = request.POST.get('userid') # will be suspended
        user_type = request.POST.get('usertype') # user type 

        global ERROR, CONTEXT, FIELD, IS_ERROR, IS_SUCCESS, SESSION

        if ( not request.session.has_key('userid') ):
            print ("Error : Your Session has been expired.")
            IS_ERROR = True
            context = { 'ERROR': ERROR, 'CONTEXT': SESSION, 'IS_ERROR': IS_ERROR }
            return render (request, self.template_name , context)
        else:

            if ( (user_id and user_id.strip()) and (user_type and user_type.strip()) ):

                    if (user_type == "Admin"):
                        suspend_admin = Admin.objects.filter(admin_id=user_id)
                        if (not(suspend_admin)):
                            print ("--------------------------------------------")
                            print ("-      Error! Admin does not exist.        -")
                            print ("--------------------------------------------")
                            IS_ERROR = True
                            context = { 'ERROR': ERROR, 'CONTEXT': CONTEXT, 'IS_ERROR': IS_ERROR }
                            return render (request, self.template_name , context)
                            #return Response ({'Error': ' Admin does not exist.'}, status=HTTP_200_OK)
                        else:
                            sus = Admin.objects.get(admin_id=user_id)
                            sus.suspend = "True"
                            sus.save()
                            print ("--------------------------------------------")
                            print ("-            Admin has been suspended.     -")
                            print ("--------------------------------------------")
                            IS_SUCCESS = True
                            IS_ERROR = False
                            context = { 'SUCCESS': SUCCESS, 'CONTEXT': SUSPENDED, 'IS_SUCCESS': IS_SUCCESS }
                            return render (request, self.template_name , context)
                            #return Response ({'Success': ' Admin has been suspended.'}, status=HTTP_200_OK)
                    elif (user_type == "User"):
                        suspend_user = User.objects.filter(user_id=user_id)
                        if (not(suspend_user)):
                            print ("--------------------------------------------")
                            print ("-            User does not exist.          -")
                            print ("--------------------------------------------")
                            IS_ERROR = True
                            context = { 'ERROR': ERROR, 'CONTEXT': CONTEXT, 'IS_ERROR': IS_ERROR }
                            return render (request, self.template_name , context)
                            #return Response ({'Error': ' User does not exist.'}, status=HTTP_200_OK)
                        else:
                            sus = User.objects.get(user_id=user_id)
                            sus.suspend = "True"
                            sus.save()
                            print ("--------------------------------------------")
                            print ("-            User has been suspended.      -")
                            print ("--------------------------------------------")
                            IS_SUCCESS = True
                            IS_ERROR = False
                            context = { 'SUCCESS': SUCCESS, 'CONTEXT': SUSPENDED, 'IS_SUCCESS': IS_SUCCESS }
                            return render (request, self.template_name , context)
                            #return Response ({'Success': ' User has been suspended.'}, status=HTTP_200_OK)
                    else:
                        print ("--------------------------------------------")
                        print ("-            Invalid User Typ              -")
                        print ("--------------------------------------------")
                        return Response ({'Error': ' invalid user type.'}, status=HTTP_200_OK)
            else:
                print ("-------------------------------------------------")
                print ("-            Empty fields                       -")
                print ("-------------------------------------------------")
                IS_ERROR = True
                context = { 'ERROR': ERROR, 'CONTEXT': FIELD, 'IS_ERROR': IS_ERROR }
                return render (request, self.template_name , context)
                #return Response({'Error': ' fields are empty.'}, status=HTTP_200_OK)


#-----------------------------------------------------------------------------------------------------
# 4 : List of User                 
#-----------------------------------------------------------------------------------------------------
def RemoveAdmin(request, delete_id):

    delete_admin = Admin.objects.filter(admin_id=delete_id)
    delete_admin.delete()
    red = redirect ('list-admin')
    return red

def RemoveUser(request, delete_id):

    delete_user = User.objects.filter(user_id=delete_id)
    delete_user.delete()
    red = redirect ('list-user')
    return red

class ListUser (APIView):

    def get(self,request):
        template_name  = "troyapi/list-user/user/base_layout.html"
        user = User.objects.all()
        arg = {'user':user }
        return render (request, template_name , arg )


#-----------------------------------------------------------------------------------------------------
# 4 : List of Admin                 
#-----------------------------------------------------------------------------------------------------
class ListAdmin (APIView):

    def get(self,request):
        template_name  = "troyapi/list-admin/admin/base_layout.html"
        admin = Admin.objects.all()
        arg = {'admin': admin}
        return render (request, template_name , arg )



#-----------------------------------------------------------------------------------------------------
# 5: Display all transactions                  
#-----------------------------------------------------------------------------------------------------
class ListTransection (APIView):

    def get(self,request):
        template_name  = "troyapi/list-transaction/transaction/base_layout.html"
        transection = Transaction.objects.all()
        arg = {'transection': transection}
        return render (request, template_name , arg )


#######################################################################################################
#                               Chat Panel API's
#######################################################################################################
# 
# 
# 
# 
#----------------------------------------------------------------------------------------------------
# 1: Signup Chat
#----------------------------------------------------------------------------------------------------
class SignupChat (APIView):
   
    queryset = ChatUser.objects.all()
    serializer_class = ChatSignupSerializer

    def get (self, request):
        template_name  = "troyapi/signup.html"
        context = {}
        return render (request, template_name , context)

    def post(self, request):
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        emailaddress = request.POST.get('email')
        password = request.POST.get('password')
        # picture = request.POST.get('picture')

        if ( (firstname and firstname.strip()) and (lastname and lastname.strip()) and (emailaddress and emailaddress.strip()) and (password and password.strip()) ):
            #unvalidEmail = Signup.objects.filter(email=email)
            useremail = ChatUser.objects.all().filter(emailaddress=emailaddress)
            
            if (not(useremail)):
                print("------------------------------------------------------------")
                print("-            User has been successfully created.           -")
                print("------------------------------------------------------------")
                mm = hashlib.md5()
                mm.update(password.encode('utf-8'))
                password = mm.hexdigest()

                # fs = FileSystemStorage ()
                # name = fs.save(picture.name, picture)
                # url = fs.url(name)
                # print ("URL : ", url)
                # url = "127.0.0.1:8000" + url
                # print ("File URL : ", url)

                newuser = ChatUser(firstname=firstname, lastname=lastname, emailaddress=emailaddress, password=password ) # Insert User to database
                newuser.save()
                
                #------------- Generating Token  -----------------------------
                tokenLength = 30
                tokenkey = ''.join(choice( str(datetime.datetime.today()) + string.ascii_uppercase+string.digits+string.ascii_lowercase ) for x in range(tokenLength))
                print ("Token Key : ",tokenkey)

                matchToken = True
                while (matchToken):
                    exist = ChatUser.objects.filter(token=tokenkey)
                    if (exist):
                        print ("I found token.")
                        tokenkey = ''.join(choice( str(datetime.datetime.today())+ string.ascii_uppercase+string.digits+string.ascii_lowercase ) for x in range(tokenLength))
                        
                    else:
                        print ("token does not found.")
                        newuser.token = tokenkey
                        newuser.save()
                        expiry_date = datetime.datetime.today() + datetime.timedelta(days=31) # Setting Expiry Date
                        newuser.timestamp = expiry_date
                        newuser.save()
                        matchToken = False

                last_user = ChatUser.objects.all().last() # getting last user details
                serializer = ChatSignupSerializer(last_user, many=False) # Convert Queryset into json formate
                # dont use lat {email firstname lastname token }           
                return Response ( serializer.data , status=HTTP_200_OK)
            else:
                print("------------------------------------------------------------")
                print("-            This email is already registed.               -")
                print("------------------------------------------------------------")
                return Response ({'Error':' This email is already registed.'}, status=HTTP_200_OK)
        else:
            print("------------------------------------------------------------")
            print("-            Fields are empty                   			  -")
            print("------------------------------------------------------------")
            return Response ({'Error':' You are missing some fields.'}, status=HTTP_200_OK) 
 

#-----------------------------------------------------------------------------------------------------
# 1: View Chat                  
#-----------------------------------------------------------------------------------------------------

class ViewChat (APIView):

    # queryset = Chat.objects.all()
    # serializer_class = ViewChatSerializer

    # def get(self,request):
    #     template_name  = "registration/view_chat.html"
    #     context = { }
    #     return render (request, template_name , context )

    def post (self, request):
        token = request.POST.get ('token') # user token who want to view chat
        viewer_id = request.POST.get ('viewer_id') # viewer id who want to view chat
        user_id = request.POST.get ('user_id') # other user id

        if ( (token and token.strip()) and (viewer_id and viewer_id.strip()) and (user_id and user_id.strip()) ):
            
            # Check : Token and id validation 
            user_tok = ChatUser.objects.filter(user_id=viewer_id, token=token)
            if (user_tok):
                print ("-------------------------------------------------------")
                print ("-                 viewer token found                  -")
                print ("-------------------------------------------------------")
                # Check: User is suspended or not
                suspend_user = ChatUser.objects.get(user_id = viewer_id)
                sus = suspend_user.suspend
                if (sus == 'True'):
                    print ("-------------------------------------------------------")
                    print ("-     Error! User has been suspended                  -")
                    print ("-------------------------------------------------------")
                    return Response ({'Error': 'User has been suspended.'}, status=HTTP_200_OK)
                else:
                    # Check: Is chat for both users exist or not 
                    sender_chat = Chat.objects.filter( sender_user_id = viewer_id, reeceiver_user_id = user_id ) | Chat.objects.filter(sender_user_id = user_id, reeceiver_user_id = viewer_id ) # sender chat to receiver
                    if (sender_chat):
                        print ("-------------------------------------------------------")
                        print ("-          list of sender message                     -")
                        print ("-------------------------------------------------------")
                        #receiver_chat = Chat.objects.filter(sender_user_id = user_id, reeceiver_user_id = viewer_id ) # receiver chat to sender
                        
                        sender_len = len(sender_chat)
                        
                        chat_len = sender_len
                        print ("Chat length: ", chat_len)
                        chat = ["" for x in range(chat_len)]

                        i=0
                        while ( i < chat_len ):
                            chat[i] = sender_chat[i]
                            i += 1

                        serializers = ViewChatSerializer(sender_chat, many=True)
                        return Response (serializers.data, status=HTTP_200_OK)
                    else:
                        print ("-------------------------------------------------------")
                        print ("-  sender and receiver ids does not found             -")
                        print ("-------------------------------------------------------")
                        return Response ({'Error': 'fields data are incorrect.'}, status=HTTP_200_OK)

            else:
                print ("-------------------------------------------------------")
                print ("-             viewer token does not found             -")
                print ("-------------------------------------------------------")
                return Response ({'Error': 'fields data are incorrect.'}, status=HTTP_200_OK)

        else:
            print ("-------------------------------------------------------")
            print ("-         ERROR! Fields are empty                     -")
            print ("-------------------------------------------------------")
            return Response ({'ERROR!': 'fields are empty'}, status=HTTP_200_OK)


#-----------------------------------------------------------------------------------------------------
# 2: Create Chat Box                  
#-----------------------------------------------------------------------------------------------------
class CreateChat (APIView):

    # queryset = Chat.objects.all()
    # serializer_class = CreateChatSerializer

    # def get(self,request):
    #     template_name  = "troyapi/create_chate.html"
    #     context = { }
    #     return render (request, template_name , context )

    def post (self, request):
        token = request.POST.get ('token') # user token who want to send message
        sender_id = request.POST.get ('sender_id') # who want to send message
        receiver_id = request.POST.get ('receiver_id') # receiver user id
        message = request.POST.get ('message') # sender message


        if ( (token and token.strip()) and (sender_id and sender_id.strip()) and (receiver_id and receiver_id.strip()) and (message and message.strip()) ):
            
            # Check : Token and id validation 
            user_tok = ChatUser.objects.filter(user_id=sender_id, token=token)
            if (user_tok):
                print ("-------------------------------------------------------")
                print ("-        message sender token found                   -")
                print ("-------------------------------------------------------")
                # Check: User is suspended or not
                suspend_user = ChatUser.objects.get (user_id = sender_id)
                sus = suspend_user.suspend
                if (sus == 'True'):
                    print ("-------------------------------------------------------")
                    print ("-        Error! User has been suspended               -")
                    print ("-------------------------------------------------------")
                    return Response ({'Error':' user has been suspended.'},status=HTTP_200_OK)
                else:
                    # Check: Is receiver user exist in database  
                    viewer = ChatUser.objects.filter( user_id = receiver_id)
                    if (viewer):
                        print ("-------------------------------------------------------")
                        print ("-               Chat box is created                   -")
                        print ("-------------------------------------------------------")
                        new_chat = Chat (sender_user_id= sender_id, reeceiver_user_id=receiver_id, message= message)
                        new_chat.save()
                        return Response ({'Success': 'message has been successuly sended.'}, status=HTTP_200_OK)
                    else:
                        print ("-------------------------------------------------------")
                        print ("-                Chat box is not created              -")
                        print ("-------------------------------------------------------")
                        return Response ({'Error': ' fields data are incorrect.'}, status=HTTP_200_OK)

            else:
                print ("-------------------------------------------------------")
                print ("-        message sender token does not found          -")
                print ("-------------------------------------------------------")
                return Response ({'Error': ' fields data are incorrect.'}, status=HTTP_200_OK)

        else:
            print ("-------------------------------------------------------")
            print ("-         ERROR! Fields are empty                     -")
            print ("-------------------------------------------------------")
            return Response ({'ERROR!': 'fields are empty'}, status=HTTP_200_OK)
