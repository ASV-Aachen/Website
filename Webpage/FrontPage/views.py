from django.shortcuts import render
from .models import Blogeintrag

# Frontpage (TODO)
def MainPage(request):
    # Eingeloggte Mitglieder bekommen eine andere Homepagemit eigenen Links und eigenen Hinweisen
    if(request.user.is_authenticated):
        return render(request, "Front_LoggedIn.html")
    return render(request, template_name="Front_NotLoggedIn.html", context={"News": Blogeintrag.objects.all().order_by('-id')[:5]})

# Mein ASV (TODO)

# News (TODO)

# neue News (TODO)
