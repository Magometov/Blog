from django.http import Http404
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth import login
from django.template.loader import get_template
from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError

from drf_spectacular.utils import extend_schema_view, extend_schema

from apps.core.models import User

# ======================================================================================================================
# Registrations
# ======================================================================================================================


@api_view(['POST'])
def send_user_data(request):
    try:
        first_name = request.data['first_name']
        last_name = request.data['last_name']
        email = request.data['email']

        if User.objects.filter(email=email).exists():
            raise ValidationError
        request.session['first_name'] = first_name
        request.session['last_name'] = last_name
        request.session['email'] = email

        return Response({"detail": "True"}, status=200)

    except ValidationError:
        return Response({'detail': 'such a user already exists!'}, status=409)
    except KeyError as e:
        return Response({'detail': f'{e} is required!'}, status=422)
    except Exception as e:
        return Response({'detail': 'Internal Server Error'}, status=500)


@api_view(['POST'])
def send_password(request):
    try:
        password = request.data['password']
        repeat_password = request.data['repeat_password']

        if password != repeat_password:
            raise ValidationError

        request.session['password'] = password

        return Response({"detail": "True"}, status=200)

    except ValidationError:
        return Response({'detail': 'passwords are not equal!'}, status=409)
    except KeyError as e:
        return Response({'detail': f'{e} is required!'}, status=422)
    except Exception as e:
        return Response({'detail': 'Internal Server Error'}, status=500)


@api_view(['GET'])
def user_registration(request):
    try:
        first_name = request.session['first_name']
        last_name = request.session['last_name']
        email = request.session['email']
        password = request.session['password']

        user = User.objects.create(
            username=email,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=make_password(password)
        )

        login(request, user)

        return Response({'detail': 'True'}, status=201)
    except KeyError as e:
        return Response({'detail': f'{e} is not in the session'}, status=409)
    except Exception as e:
        return Response({'detail': 'Internal Server Error'}, status=500)

# ======================================================================================================================
# Registrations
# ======================================================================================================================


@api_view(['POST'])
def email_verify_view(request):
    try:
        email = request.data['email']
        user = get_object_or_404(User, email=email)
        request.session['email'] = email
        return Response({'detail': 'True'}, status=200)
    except KeyError as e:
        return Response({'detail': f'{e} is required!'}, status=422)
    except Http404:
        return Response({'detail': 'user not found'}, status=404)
    except Exception as e:
        return Response({'detail': 'Internal Server Error'}, status=500)


@api_view(['POST'])
def email_password_verify_view(request):
    try:
        if not 'email' in request.session:
            raise ValidationError
        user = get_object_or_404(User, email=request.session.get('email'))
        password = request.data['password']
        if check_password(password, user.password):
            return Response({'detail': 'True'}, status=200)
        else:
            return Response({'detail': 'False'}, status=403)
    except ValidationError:
        return Response({'detail': 'email is not in the session'}, status=409)
    except KeyError as e:
        return Response({'detail': f'{e} is required!'}, status=422)
    except Http404:
        return Response({'detail': 'user not found'}, status=404)
    except Exception as e:
        return Response({'detail': 'Internal Server Error'}, status=500)
