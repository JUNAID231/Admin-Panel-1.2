


from django.urls import path, include
from . import views

urlpatterns = [

    # ------------------------------------------------------------------------------
    #                   APIs
    # -----------------------------------------------------------------------------
    # Registration
    path ('user/signin/', views.SigninUser.as_view(), name="signin"), # Sign url for the user
    path ('user/signup/', views.SignupUser.as_view(), name="signup"), # Signup url to create new user

    # Transaction via Email
    path('user/transfer/', views.TransferFund.as_view(), name="transfer"), # send transaction via email id
    path ('user/recevied/', views.Amount.as_view(), name="recevier"), # check you amount via email id
    path ('user/status/', views.ConfirmStatus.as_view(), name='confirm'), # recevie amount and update recored

    # Chat
    path ('user/signup-chat/',views.SignupChat.as_view(), name="signup-chat"), # View a specfic chat

    path ('user/view-chat/',views.ViewChat.as_view(), name="view-chat"), # View a specfic chat
    path ('user/create-chat/',views.CreateChat.as_view(), name="create-chat"), # creat new chat

    # News
    path ('list-news/', views.ListNews.as_view(), name='list-news'),
    


    # ------------------------------------------------------------------------------------
    #                   Admin Panel Interface
    # ------------------------------------------------------------------------------------
    # Registration: Admin Penel 
    path('admin/signin/', views.SigninAdmin.as_view(), name="admin-signin"), # Admin Interface
    path('admin/signout/', views.SignoutAdmin.as_view(), name="admin-signout"), # Admin Interface
    
    # User: Admin Panel
    path('admin/create-user/', views.CreateAdmin.as_view(), name="create-user"), # Admin Interface: add new admin to the database
    path('admin/delete-user/', views.DeleteAdmin.as_view(), name="delete-user" ), # Admin Interface: take admin validation and redirect it to next page
    path ('admin/edit-user/',views.EditUser.as_view(), name="edit-user"), # Admin Interface: take admin validations
    path ('admin/redirect-edit-user/',views.RedirectEditUser.as_view(), name="redirect-edit-user"), # Admin Interface: take admin validations
    path ('admin/suspend-user/',views.Suspend.as_view(), name="suspend-user"), # Admin Interface
    
    path ('removeuser/<int:delete_id>/',views.RemoveUser, name="removeuser"), 
    path ('admin/list-user/',views.ListUser.as_view(), name="list-user"), # Admin Interface
    path ('edit/<str:user_type>/<int:user_id>/',views.EditUserW, name="edituser"),

    path ('removeadmin/<int:delete_id>/',views.RemoveAdmin, name="removeadmin"), 
    path ('admin/list-admin/',views.ListAdmin.as_view(), name="list-admin"), # Admin Interface
    
    # Transaction List: Admin Panel 
    path ('admin/list-transections/',views.ListTransection.as_view(), name="list-transections"), # Admin Interface
    
    # News: Admin Panel 
    path('testing/<int:news_id>/', views.CallMe, name='test'),
    path('remove/<int:delete_id>/', views.Remove, name='remove'),
    path('admin/add-news/', views.AddNews.as_view(), name='add-news'),
    path('admin/edit-news/', views.EditNews, name='edit-news'),
    path('admin/redirect-edit-news/', views.RedirectEditNews.as_view(), name='redirect-edit-news'),
    path ('admin/delete-news/', views.DeleteNews.as_view(), name='delete-news'),
    path ('admin/list-news/', views.ListNewsIneterface.as_view(), name='list-news-interface') # Admin Interface

] 