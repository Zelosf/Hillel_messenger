from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponseForbidden, JsonResponse
from django.core.paginator import Paginator
from django.contrib import messages
from .models import Chat, UserStatus


class CustomLoginRequiredMixin(LoginRequiredMixin):
	login_url = '/login/'
	redirect_field_name = 'redirect_to'


class CustomPermissionRequiredMixin(PermissionRequiredMixin):
	permission_denied_message = 'You do not have permission to access this page.'


class UserIsParticipantMixin:
	def dispatch(self, request, *args, **kwargs):
		chat_id = kwargs.get('chat_id')
		try:
			chat = Chat.objects.get(id=chat_id)
			if request.user not in chat.participants.all():
				return HttpResponseForbidden("You are not a participant of this chat.")
		except Chat.DoesNotExist:
			return HttpResponseForbidden("Chat not found.")
		return super().dispatch(request, *args, **kwargs)


class SuperUserRequiredMixin:
	def dispatch(self, request, *args, **kwargs):
		if not request.user.is_superuser:
			return HttpResponseForbidden("You must be a superuser to access this page.")
		return super().dispatch(request, *args, **kwargs)


class JsonResponseMixin:
	def render_to_json_response(self, context, **response_kwargs):
		return JsonResponse(context, **response_kwargs)


class FormValidMessageMixin:
	success_message = "Form submission successful."

	def form_valid(self, form):
		response = super().form_valid(form)
		messages.success(self.request, self.success_message)
		return response


class ObjectOwnerMixin:
	def dispatch(self, request, *args, **kwargs):
		obj = self.get_object()
		if obj.author != request.user:
			return HttpResponseForbidden("You are not the owner of this object.")
		return super().dispatch(request, *args, **kwargs)


class PaginateMixin:
	paginate_by = 10

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		paginator = Paginator(self.get_queryset(), self.paginate_by)
		page = self.request.GET.get('page')
		context['page_obj'] = paginator.get_page(page)
		return context


class FilterQuerySetMixin:
	filter_field = None

	def get_queryset(self):
		queryset = super().get_queryset()
		filter_value = self.request.GET.get(self.filter_field)
		if filter_value:
			queryset = queryset.filter(**{self.filter_field: filter_value})
		return queryset


class ContextDataMixin:
	extra_context = {}

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context.update(self.extra_context)
		return context
