# Django imports
from django.contrib.auth import get_user_model

# Rest imports
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.routers import SimpleRouter, Route
from rest_framework import status

# Project imports
from project.api.serializers.inauth import (
    AuthSerializer,
    ForgotPasswordSerializer,
    ResetPasswordSerializer
)
from project.inauth.auth import Auth
from project.inauth.models import PasswordResetRequest
from project.utils.utils import get_username_from_email

User = get_user_model()


class InauthRouter(SimpleRouter):

    routes = [
        Route(
            url=r'login/$',
            mapping={
                'post': 'login_or_register'
            },
            name='{basename}-login',
            initkwargs={}
        ),
        Route(
            url=r'forgot-password/$',
            mapping={
                'post': 'forgot_password'
            },
            name='{basename}-forgot-password',
            initkwargs={}
        ),
        Route(
            url=r'reset-password/$',
            mapping={
                'post': 'reset_password'
            },
            name='{basename}-reset-password',
            initkwargs={}
        ),
    ]


class InauthViewSet(viewsets.ViewSet):
    """
    Base api class for login and registration actions.
    """

    def login_or_register(self, request, **kwargs):
        auth = AuthSerializer(data=request.data)
        # auth.is_valid(raise_exception=True)

        email = request.data.get('email')
        name = request.data.get('name')
        kwargs = {
            'name': name or get_username_from_email(email),
        }

        inauth = Auth(
            email=email,
            password=request.data.get('password'),
            **kwargs
        )

        if not inauth.is_valid():
            return Response({
                    'errors': inauth.get_errors(),
                })
        else:
            action, user = inauth.login_or_register(request)
            return Response({
                    'token': user.api_token
                })

    def forgot_password(self, request, **kwargs):
        forgot_password = ForgotPasswordSerializer(data=request.data)
        forgot_password.is_valid(raise_exception=True)

        email = request.data.get('email')
        forgot_password.apply_reset(email)
        return Response({
                'answer': True
            })

    def reset_password(self, request, **kwargs):
        reset_request = ResetPasswordSerializer(data=request.data)
        reset_request.is_valid(raise_exception=True)

        new_password = request.data.get('password')
        key = request.data.get('key')

        reset_request = PasswordResetRequest.objects.filter(key=key, used=False).first()
        user = User.objects.get(email=reset_request.email)
        user.set_password(new_password)
        user.save()

        reset_request.mark_as_used()
        return Response({'answer': True})
