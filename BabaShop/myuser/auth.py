from django.contrib import messages
from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect


class LoginRequiredMixin(AccessMixin):
    """
    Verify that the current user is
    authenticated and is supplier
    """
    def dispatch(self, request, *args, **kwargs):
        if not (request.user.is_authenticated and request.user.is_supplier):
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class PhoneVerifyRequiredMixin(AccessMixin):
    """
    Verify that the current user phone is phone verified
    """
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_phone_verified:
            messages.error(request, "You must first verity your phone" )
            return redirect('supplier_phone_verify_url')
        return super().dispatch(request, *args, **kwargs)
