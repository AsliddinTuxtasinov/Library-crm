from django.urls import path

from apps.ausers import views

urlpatterns = [
    path("login", views.LoginRegisterUserViews.as_view()),
    path("login/refresh", views.LoginRefreshViews.as_view()),
    path("confirm-verify-code", views.ConfirmVerifyCodeView.as_view()),
    path("update-user-auth", views.UpdateUserAuthView.as_view()),
    path("authenticate", views.LoginViews.as_view()),
    path("new-verify", views.GetNewVerificationCode.as_view()),
]
