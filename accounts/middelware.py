from django.shortcuts import redirect, render, HttpResponseRedirect






def auth_middleware(get_response):
	def middleware(request):
		returnUrl = request.META['PATH_INFO']
		if not request.user.is_authenticated:
			return redirect(f'http://127.0.0.1:8000/accounts/login/?return_url={returnUrl}')
		response = get_response(request)
		return response
	return middleware