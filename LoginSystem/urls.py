from django.urls import path
from .views import LoginViews

urlpatterns = [

    path('',LoginViews.Home_th,name='home-th'),
    path('home-en',LoginViews.Home_en,name='home-en'),
    path('login-th/',LoginViews.LoginView,name='login-th'),
    path('register-th/',LoginViews.RegisterView,name='register-th'),
    path('logout/',LoginViews.LogoutView,name='logout'),

   # path('reserve/',LoginViews.ReserveView,name='reserve'),

    #path('big-reservation/',LoginViews.BigReserveView,name='bigreserve'),
    #path('medium-reservation/',LoginViews.MediumReserveView,name='mediumreserve'),
    #path('small-reservation/',LoginViews.SmallReserveView,name='smallreserve'),
    
    path('forgotpassword/',LoginViews.ForgotPassword,name = 'forgot-password'),
    path('password-reset-sent/<str:reset_id>/', LoginViews.PasswordResetSent, name='password-reset-sent'),
    path('reset-password/<str:reset_id>/', LoginViews.ResetPassword, name='reset-password'),
    
    path('my-reservations/', LoginViews.my_reservations, name='my-reservations'),
    path('update-profile/', LoginViews.update_user_profile, name='update-profile'),
    path('change-password/', LoginViews.change_password, name='change-password'),
    path('api/users/<int:user_id>/update/', LoginViews.update_user, name='update-user'),

    path('about-us/', LoginViews.AboutusView, name='aboutus'),
    path('myaccount/', LoginViews.UserEditView, name='edituser'),

    path("gallery/", LoginViews.gallery_view, name="gallery"),

    path("contact-us/", LoginViews.contactUsView, name="contactUs"),
    path("guide/", LoginViews.guideView, name="guide")
    #for test
    #path('passwordresetfortesting/', LoginViews.PasswordResetSentForTesting, name='passwordresettest'),
    
]
