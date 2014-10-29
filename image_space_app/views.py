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
from image_space_app.forms import UserForm, UserProfileForm

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
            return redirect('/profile/')
        
        user.userpicture_set.create(picture=picture, title=request.POST['title']).save()
        user.save()
        messages.info(request, "Picture uploaded")
        return redirect('/profile/')

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
            return redirect('/')

        return render( request, template, {'picture': picture})

    @method_decorator(login_required)
    def post(self, request, pk):
        picture = UserPicture.objects.get(pk=pk)
        owned = False
        user = request.user

        if picture in user.userpicture_set.all():
            owned = True

        if not owned:
            return redirect('/')

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
            user_img_url = user.userprofile.picture.url
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
    return redirect('/')

class LoginUserView(View):
    def post(self, request):
        logout(request)
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)

                return redirect('/profile')
            else:
                messages.info(request, "Inactive user")
        else:
            messages.info(request, "Bad login info")

        return render(request, 'image_space_app/login/login.html')

    def get(self, request):
        return render(request, 'image_space_app/login/login.html')

class RegisterView(View):
    http_method_names = ['get', 'post']
    def get(self, request):
        logout(request)
        registered = False
        user_form = UserForm()
        profile_form = UserProfileForm()
        return render(request, 'image_space_app/register/register.html',
                      {'user_form': user_form, 'profile_form': profile_form,
                       'registered': registered})

    def post(self, request):
        logout(request)
        registered = False
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()

            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()
            registered = True

            return redirect('/profile')
        else:
            return render(request, 'image_space_app/register/register.html',
                      {'user_form': user_form, 'profile_form': profile_form,
                       'registered': registered})