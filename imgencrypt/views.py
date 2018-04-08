from django.shortcuts import render, HttpResponse, redirect
import imgencrypt.sdes as sdes

# Create your views here.

def Index(request):
     if request.method == 'POST':
        file=request.FILES['file']
        value=request.POST['submit']
        if value == 'encrypt':
            filename=sdes.encryption(file)
        else:
            filename=sdes.decryption(file)
        return redirect('img',filename)
     return render(request,'index.html')

def Img(request,name):
    return render(request,'image.html',{'name':name})
