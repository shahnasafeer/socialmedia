from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import login,authenticate,logout
from django.views import View
from django.views.generic.base import View
from django.contrib import messages
from django.http import JsonResponse
from django.views.generic import View,CreateView,ListView,DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post,Comment,Profile,About,Follow,Like,Notification,Mention,Message
from django.contrib.auth.forms import AuthenticationForm,PasswordResetForm
from django.contrib.auth.models import User
from .forms import SignInForm, CustomUserCreationForm,PostForm,AboutForm,ProfilePicForm,CommentForm,MessageForm
from django.views import View
import logging
import json
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

class IndexView(View):
    def get(self, request):
            about_data = About.objects.filter(userid=request.user)
            profile_data = Profile.objects.all()
            post_data = Post.objects.all().order_by('-created_at')
            form = CommentForm()  
            suggested_users = User.objects.exclude(pk=request.user.pk)
            following_users = Follow.objects.filter(follower=request.user).values_list('followed', flat=True)
            suggested_users = suggested_users.exclude(pk__in=following_users)
            user_messages = Message.objects.filter(recipient=request.user)
            user_post = Post.objects.filter(userid=request.user)

            context = {
            'index': {
                'about_data': about_data,
                'profile_data': profile_data,
                'post_data': post_data,
                'suggested_users': suggested_users,
                'user_messages': user_messages,
                'user_post': user_post,
                'comment_form': form, 
            },
        }
            return render(request, 'index.html', context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        suggested_users = User.objects.exclude(pk=self.request.user.pk)
        context['suggested_users'] = suggested_users
        return context
class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        user_posts = Post.objects.filter(userid=request.user)
        post_count = request.user.post_set.count()
        return render(request,'profile.html', {'user_posts': user_posts, 'post_count': post_count})

class NotificationView(View):
    def get(self, request):
        user_notifications = Notification.objects.filter(user=request.user).select_related('post').order_by('-created_at')
        user_posts = Post.objects.filter(userid=request.user)
        suggested_users = User.objects.exclude(pk=request.user.pk)
        
        context = {
           'notifications': user_notifications,
           'user_posts': user_posts,
           'suggested_users': suggested_users,
        }
        
        return render(request, 'notification.html', context)

class SignUp(View):
    def get(self, request):
        form = CustomUserCreationForm()
        return render(request,'signup.html', {'form': form})
    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('signin') 
        return render(request,'signup.html', {'form': form})
class SignOutView(View):
    def get(self, request):
        if request.user.is_authenticated:
            logout(request)
            messages.success(request, 'You have been successfully logged out.')
        return redirect('signin')
    
class LoginView(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'signin.html', {'form': form})

    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                request.session['id'] = user.id
                return redirect('index')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid form submission. Please check the form data.')

        return render(request, 'signin.html', {'form': form})
class AboutView(LoginRequiredMixin, View):
    def get(self, request, pk=None):
        context = {}

        if pk:
            instance = get_object_or_404(About, pk=pk)
            if instance.userid_id != request.user.id:
                return redirect('index')
            form = AboutForm(instance=instance)
            context['form'] = form
            context['instance'] = instance
        else:
            form = AboutForm()
            data = About.objects.filter(userid=request.user)
            context['form'] = form
            context['data'] = data

        about_data = About.objects.filter(userid=request.user)
        user_post = Post.objects.filter(userid=request.user)
        suggested_users = User.objects.exclude(pk=request.user.pk)
        context['suggested_users'] = suggested_users
        context['user_post'] = user_post
        context['about_data'] = about_data

        return render(request, 'Aboutt.html', context)

    def post(self, request, pk=None):
        instance_id = request.POST.get('instance')
        if instance_id:
            instance = get_object_or_404(About, pk=instance_id)
            if instance.userid_id != request.user.id:
                return redirect('index')
            form = AboutForm(request.POST, request.FILES, instance=instance)
        else:
            form = AboutForm(request.POST, request.FILES)

        if form.is_valid():
            about_instance = form.save(commit=False)
            about_instance.userid = request.user 
            about_instance.save()
            return redirect('index')
        else:
            if pk:
                data = About.objects.filter(userid=request.user)
                return render(request, 'Aboutt.html', {'form': form, 'data': data, 'pk': pk})
            else:
                return render(request, 'Aboutt.html', {'form': form})

class EditAboutView(View):
    def get(self, request, pk):
        about_instance = get_object_or_404(About, pk=pk)
        form = AboutForm(instance=about_instance)
        return render(request, 'Aboutt.html', {'form': form, 'instance': about_instance})

    def post(self, request, pk):
        about_instance = get_object_or_404(About, pk=pk)
        form = AboutForm(request.POST, instance=about_instance)
        if form.is_valid():
            form.save()
            return redirect('index')
        return render(request, 'Aboutt.html', {'form': form, 'instance': about_instance})
class AddProfileView(View):
    def get(self, request, pk=None):
        if pk is not None:
            instance1 = Profile.objects.get(pk=pk)
            form = ProfilePicForm(instance=instance1)
            return render(request, 'user_profile.html', {'form': form, 'instance': instance1})
        else:
            form = ProfilePicForm()
            data = Profile.objects.all()
            return render(request, 'user_profile.html', {'form': form, 'data': data})
   
    def post(self, request, pk=None):
        instance_id = request.POST.get('instance')
        if instance_id:
            instance = Profile.objects.get(pk=instance_id)
            form = ProfilePicForm(request.POST, request.FILES, instance=instance)
        else:
            form = ProfilePicForm(request.POST, request.FILES)

        if form.is_valid():
            profile = form.save(commit=False)
            profile.name = request.user  
            profile.save()
            return redirect('index')
        else:
            data = Profile.objects.all()
            return render(request, 'user_profile.html', {'form': form, 'data': data})

class PostView(View):
    def get(self, request, pk=None):
        if pk is not None:
            instance = Post.objects.get(pk=pk)
            form = PostForm(instance=instance)
            return render(request, 'posts.html', {'form': form, 'instance': instance})
        else:
            form = PostForm()
            user_posts = Post.objects.filter(userid=request.user)
            return render(request, 'posts.html', {'form': form, 'user_posts': user_posts})

    def post(self, request, pk=None):
        if pk:
            instance = Post.objects.get(pk=pk)
            form = PostForm(request.POST, request.FILES, instance=instance)
        else:
            form = PostForm(request.POST, request.FILES)

        if form.is_valid():
            post = form.save(commit=False)
            post.userid = request.user
            post.save()
            post.create_notifications()
            form.save_m2m()
            messages.success(request, 'Post submitted successfully!')
            return redirect('index')
        else:
            user_posts = Post.objects.filter(userid=request.user)
            return render(request, 'posts.html', {'form': form, 'user_posts': user_posts})
    
class DeletePostView(View):
    def get(self, request, pk):
        post = Post.objects.get(pk=pk)
        post.delete()
        return redirect('index')
class FollowUserView(View):
    def post(self, request, user_id):
        user_to_follow = get_object_or_404(User, pk=user_id)
        if not Follow.objects.filter(follower=request.user, followed=user_to_follow).exists():
            Follow.objects.create(follower=request.user, followed=user_to_follow)
            messages.success(request, f"You followed {user_to_follow.username} successfully!")
            Notification.objects.create(
                user=user_to_follow, 
                type='follow', 
                message=f'{request.user.username} started following you.'
            )
        else:
            messages.info(request, f"You are already following {user_to_follow.username}.")
        return redirect('index')
class LikePostView(View):
    def post(self, request):
        if request.user.is_authenticated: 
            post_id = request.POST.get('post_id')
            post = get_object_or_404(Post, pk=post_id)
            if not Like.objects.filter(user=request.user, post=post).exists():
                like = Like.objects.create(user=request.user, post=post)
                post.likes.add(request.user)  

                
                Notification.objects.create(
                    user=post.userid, 
                    message=f'{request.user.username} liked your post.',
                    post=post
                )
                
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'error': 'User has already liked this post'})
        else:
            return JsonResponse({'success': False, 'error': 'User not authenticated'})
        
logger = logging.getLogger(__name__)
class CommentView(View):
    def post(self, request):
        logger.debug(f'Request POST data: {request.POST}')
        comment_id = request.POST.get('comment_id')
        post_id = request.POST.get('post_id')
        comment_text = request.POST.get('text')

        if comment_id:
            # Editing an existing comment
            comment = get_object_or_404(Comment, id=comment_id)
            comment.text = comment_text
            comment.save()
            return JsonResponse({
                'success': True,
                'comment_id': comment.id,
                'comment_text': comment.text,
                'commenter_username': comment.user.username,
                'commenter_image_url': comment.user.profile.image.url if comment.user.profile.image else '/static/img/default_avatar.jpg'
            })
        else:
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                try:
                    comment.post = Post.objects.get(id=post_id)
                except Post.DoesNotExist:
                    return JsonResponse({'success': False, 'error': 'Invalid post ID.'})
                comment.user = request.user
                comment.save()
                return JsonResponse({
                    'success': True,
                    'comment_id': comment.id,
                    'comment_text': comment.text,
                    'commenter_username': comment.user.username,
                    'commenter_image_url': comment.user.profile.image.url if comment.user.profile.image else '/static/img/default_avatar.jpg'
                })
            else:
                logger.error(f'Form errors: {form.errors}')
                return JsonResponse({'success': False, 'error': 'Error submitting comment.'})
class SearchUsersView(View):
    def get(self, request):
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            query = request.GET.get('query', None)
            if query:
                results = User.objects.filter(username__icontains=query)
                data = [{'username': profile.username} for profile in results]
                return JsonResponse(data, safe=False)
        return JsonResponse([], safe=False)
################################################################

class UsersListView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        send_messages = Message.objects.filter(sender=request.user)
        receive_messages = Message.objects.filter(recipient=request.user)
        users = User.objects.exclude(id=request.user.id)  # Fetch all users except the logged-in user
        return render(request, 'all_users_list.html', {
            'send_messages': send_messages,
            'receive_messages': receive_messages,
            'users': users,
        })
class SendMessageView(LoginRequiredMixin, CreateView):
    model = Message
    fields = ['message_content']
    template_name = 'send_message.html'
    success_url = '/inbox/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = User.objects.exclude(id=self.request.user.id)
        context['recipient'] = get_object_or_404(User, id=self.kwargs['recipient_id'])
        return context

    def form_valid(self, form):
        form.instance.sender = self.request.user
        form.instance.recipient = get_object_or_404(User, id=self.kwargs['recipient_id'])
        return super().form_valid(form)
@login_required
def get_user_messages(request, user_id):
    if request.user.id != user_id:
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    messages = Message.objects.filter(recipient_id=user_id).exclude(sender_id=request.user.id)
    return JsonResponse([{
        'sender': {
            'username': message.sender.username,
            'profile': {
                'image': {
                    'url': message.sender.profile.image.url
                }
            }
        },
        'message_content': message.text,
        'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S')
    } for message in messages], safe=False)

class GetMessagesView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        messages = Message.objects.filter(recipient=request.user).values('recipient_id', 'sender_id', 'text', 'timestamp')
        messages_list = list(messages)
        return JsonResponse({'messages': messages_list})

class InboxView(LoginRequiredMixin, ListView):
    model = Message
    context_object_name = 'messages'
    template_name = 'inbox.html'

    def get_queryset(self):
        return Message.objects.filter(recipient=self.request.user).exclude(sender=self.request.user)

@login_required
def user_messages(request, recipient_id):
    if request.user.id != recipient_id:
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    messages = Message.objects.filter(recipient_id=recipient_id, sender__ne=request.user)
    return JsonResponse([{
        'sender': {
            'username': message.sender.username,
            'profile': {
                'image': {
                    'url': message.sender.profile.image.url
                }
            }
        },
        'message_content': message.text,  # Ensure this matches the field name in your model
        'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S')
    } for message in messages], safe=False)


class SendMessageView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        recipient_id = kwargs.get('recipient_id')
        message_text = data.get('message')

        # Ensure recipient_id and message_text are provided
        if not recipient_id or not message_text:
            return JsonResponse({'error': 'Invalid data'}, status=400)

        try:
            recipient = User.objects.get(id=recipient_id)
        except User.DoesNotExist:
            return JsonResponse({'error': 'Recipient not found'}, status=404)

        message = Message.objects.create(
            sender=request.user,
            recipient=recipient,
            text=message_text
        )

        return JsonResponse({
            'sender': {'username': request.user.username},
            'recipient': {'username': recipient.username},
            'text': message.text,
            'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        })
    
