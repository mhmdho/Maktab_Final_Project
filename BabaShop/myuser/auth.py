from django.contrib.auth.mixins import AccessMixin



class LoginRequiredMixin(AccessMixin):
    """
    Verify that the current user is authenticated,
    is supplier and is phone verified
    """
    def dispatch(self, request, *args, **kwargs):
        if not (request.user.is_authenticated and request.user.is_supplier):
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)