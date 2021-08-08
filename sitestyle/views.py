from django.shortcuts import render


def style_test(request):
    return render(request, "sitestyle/style_test.html", {})
