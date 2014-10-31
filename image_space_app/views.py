# Stuff
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import redirect, render
from django.core.context_processors import csrf
from django.contrib.auth import authenticate, login, logout

# Decorators
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Generic views
from django.views.generic import View, TemplateView, ListView, CreateView
from django.views.generic import DetailView

# Pagination and messages framework
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages

# Models
from image_space_app.models import UserPicture, User, UserProfile

# Forms
from image_space_app.forms import UserForm, UserProfileForm, UserPictureForm

# ImageKit Spec
from imagekit import ImageSpec
from imagekit.processors import Adjust

from django.core.files.base import ContentFile
from django.core.urlresolvers import reverse
from django.core.files import File


# This class is ready
class RootView(TemplateView):
    http_method_names = ['get']
    template_name = 'image_space_app/home.html'

    # So the pictures in the home page render
    def get_context_data(self, **kwargs):
        context = super(RootView, self).get_context_data(**kwargs)
        context['latest_pictures'] = UserPicture.objects.all()[:10]
        return context

# This class is ready
class PictureUpload(View):
    http_method_names = ['get', 'post']
    
    @method_decorator(login_required)
    def get(self, request):
        template_name = 'image_space_app/pictures/upload.html'
        return render( request, template_name )

    @method_decorator(login_required)
    def post(self, request):
        user = request.user

        if 'new_picture' in request.FILES:
            picture = request.FILES['new_picture']
        else:
            return redirect(reverse('profile'))
        
        user.userpicture_set.create(picture=picture, title=request.POST['title']).save()
        user.save()
        messages.info(request, "Picture uploaded")
        return redirect(reverse('profile'))

# This class is ready
class PicturesList(ListView):
    http_method_names = ['get', 'head']
    model = UserPicture 
    template_name = 'image_space_app/pictures/list.html'
    context_object_name = 'pictures'
    paginate_by = 9

# This class is almost ready (Still have to figure out how to integrate imagekit)
class PictureEdit(View):
    @method_decorator(login_required)

    def get(self, request, pk):
        template = 'image_space_app/pictures/edit.html'
        picture = UserPicture.objects.get(pk=pk)
        owned = False
        user = request.user

        if picture in user.userpicture_set.all():
            owned = True

        if not owned:
            return redirect(reverse('home'))

        return render( request, template, {'picture': picture})

    @method_decorator(login_required)
    def post(self, request, pk):
        picture = UserPicture.objects.get(pk=pk)
        owned = False
        user = request.user

        if picture in user.userpicture_set.all():
            owned = True

        if not owned:
            return redirect(reverse('home'))

        bright = float(request.POST["brightness"]) / 200 + 0.5
        print bright
        gen = Brightness(source=picture.picture)
        gen.set_processor(bright)
        new_picture = gen.generate()
        picture.picture.save(picture.picture.url, File(new_picture))        
        messages.info(request, "Successful edit")
        return redirect(reverse('picture_details', args=(pk,)))

class Brightness(ImageSpec):
    format = 'JPEG'
    def set_processor(self, bright):
        self.processors=[ Adjust(brightness=bright)]

# This class is ready
class PictureDetails(DetailView):
    http_method_names = ['get']
    template_name = 'image_space_app/pictures/details.html'
    model = UserPicture
    context_object_name = 'picture'

# This class is ready
class ProfileDetails(View):
    http_method_names = ['get']

    def get(self, request):
        template_name = 'image_space_app/profile.html'
        context = {}
        user = self.request.user

        try:
            user_img_url = user.userprofile.picture.picture.url
        except:
            user_img_url = ""

        context['user_img'] = user_img_url
        
        try:
            user_pictures_list = user.userpicture_set.all()
            paginator = Paginator(user_pictures_list, 3)
            
            page = request.GET.get("page")

            try:
                user_pictures = paginator.page(page)
            except PageNotAnInteger:
                user_pictures = paginator.page(1)
            except EmptyPage:
                user_pictures = paginator.page(paginator.num_pages)
        except:
            user_pictures = None

        
        if user_pictures is not None:
            number_of_pages = range(1, paginator.num_pages + 1)
            context['pictures'] = user_pictures.object_list
            context['page_obj'] = user_pictures
            context['paginator'] = paginator
            context['number_of_pages'] = number_of_pages
        
        return render (request, template_name, context)

@login_required
def log_out(request):
    logout(request)
    return redirect(reverse('home'))

def log_in(username, password, request, callback_success=None, 
           callback_inactive=None, callback_fail=None):
    user = authenticate(username=username, password=password)
    print user
    if user is not None:
        if user.is_active:
            login(request, user)
            if callback_success is not None:
                callback_success()
            else:
                return redirect(reverse('profile'))
        else:
            if callback_inactive is not None:
                callback_inactive()
            else:
                messages.info(request, "Inactive user")
    else:
        if callback_fail is not None:
            callback_fail()
        else:
            messages.info(request, "Bad login info")
    return None

class LoginUserView(View):
    def post(self, request):
        logout(request)
        username = request.POST['username']
        password = request.POST['password']
        
        redirect_maybe = log_in(username, password, request)

        if redirect_maybe is not None:
            return redirect_maybe

        return render(request, 'image_space_app/login/login.html')

    def get(self, request):
        return render(request, 'image_space_app/login/login.html')

class ProfilePictureChange(View):
    http_method_names = ['post']
    
    @method_decorator(login_required)
    def post(self, request, pk):
        picture = UserPicture.objects.get(pk=pk)
        request.user.userprofile.picture = picture
        request.user.userprofile.save()
        return redirect(reverse('profile'))

class RegisterView(View):
    http_method_names = ['get', 'post']
    def get(self, request):
        logout(request)
        registered = False
        user_form = UserForm()
        profile_form = UserProfileForm()
        picture_form = UserPictureForm()
        return render(request, 'image_space_app/register/register.html',
                      {'user_form': user_form, 'profile_form': profile_form,
                       'picture_form': picture_form, 'registered': registered})

    def post(self, request):
        logout(request)
        registered = False
        user_form = UserForm(data=request.POST)
        
        if user_form.is_valid():
            user = user_form.save()
            password = user.password
            user.set_password(user.password)
            user.save()
            
            if 'picture' in request.FILES:
                picture = UserPicture.objects.create(user=user, picture=request.FILES['picture'])
                picture.save()
            else:
                picture = None

            profile = UserProfile()
            profile.user = user
            profile.picture = picture
            profile.save()

            registered = True
            
            redirect_maybe = log_in(user.username, password, request)

            if redirect_maybe is not None:
                return redirect_maybe

        else:
            print "user"
            print user_form.errors
            print "picture"
            print  picture_form.errors
            return render(request, 'image_space_app/register/register.html',
                      {'user_form': user_form,
                       'picture_form': picture_form, 'registered': registered})