from rest_framework import serializers
from .models import User, Transaction, News, Admin, Chat, ChatUser


#--------------------  User Registration  -----------------------------------------------------------
class SignupSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        #fields = '__all__'
        fields = ('firstname','lastname','emailaddress','signup_token')

class SigninSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        #fields = '__all__'
        fields = ('emailaddress','password')

# class SignoutSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         #fields = '__all__'
#         fields = ('walletid')

#--------------    Transaction via Email  ----------------------------------------------------------
class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        #fields = '__all__'
        fields = ('to_emailaddress', 'amount', 'transaction_code')

class CheckAmountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('from_walletID','to_walletID','to_emailaddress','amount','status','transaction_code')


#-----------------------------   News   ----------------------------------------------------------
class AddNewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        #fields = '__all__'
        fields = ('category', 'title', 'short_description', 'long_description', 'auther')
class ListNewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        #fields = '__all__'
        fields = ('category', 'title', 'short_description', 'long_description', 'auther')

class EditNewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        #fields = '__all__'
        fields = ('category','title','short_description','long_description','photo','auther')

class SearchAutherSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        #fields = '__all__'
        fields = ('category','auther')

#---------------- Admin Panel  ---------------------------------------------------------------------
class AddAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = ('firstname','lastname','emailaddress','password')


#----------------     Chat  --------------------------------------------------------------------------
class ChatSignupSerializer (serializers.ModelSerializer):
    class Meta:
        model = ChatUser
        # field = '__all___'
        fields = ('firstname','lastname','emailaddress','token')

class ViewChatSerializer (serializers.ModelSerializer):
    class Meta:
        model = Chat
        # field = '__all___'
        fields = ('sender_user_id','reeceiver_user_id','message','timestamp')

class CreateChatSerializer (serializers.ModelSerializer):
    class Meta:
        model = Chat
        # field = '__all___'
        fields = ('sender_user_id','reeceiver_user_id','message','timestamp')

