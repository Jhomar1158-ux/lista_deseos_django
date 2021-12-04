from django.shortcuts import render, redirect
from django.contrib import messages
from app1.models import user, items

import re
import bcrypt

# Create your views here.

NAME_REGEX = re.compile(r'^[a-zA-Z]+$')

def index(request):
    if 'login' not in request.session:
        request.session['login'] = False
    
    if 'u_id' not in request.session:
        request.session['u_id'] = 0

    return render(request, 'index.html')

def registro(request):

    check = user.objects.filter(username = request.POST['username'])
    
    error = False
    
    # NOMBRE Y USERNAME

    if len(request.POST['name'])< 3:
        messages.error(request,'Tu nombre debe tener al menos 3 carácteres.', extra_tags = 'fn_error' )
        error = True

    if len(request.POST['username'])< 3:
        messages.error(request,'Tu usuario debe tener al menos 3 carácteres.', extra_tags = 'ln_error')
        error = True
    
    # username_error -> email_error ***** CORREGIR
    if check:
        messages.error(request,'Este usuario ya se encuentra registrado', extra_tags = 'username_error')
        error = True

    # PASSWORD, CONFIRM PASSWORD 

    if request.POST['password'] != request.POST['confirm_password']:
        messages.error(request,'Las contraseñas no coinciden', extra_tags = 'pw_error')
        error = True

    if len(request.POST['password']) < 8 :
        messages.error(request,'Tu contraseña debe teener al menos 8 carácteres', extra_tags = 'pw_error')

    
    
    # =======================================

    if error == True:
        return redirect('/')

    elif error == False:
        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        new_user = user.objects.create(name = request.POST['name'], username = request.POST['username'], release_date=request.POST['release_date'], password = pw_hash)
        print(new_user)
        request.session['user_id'] = new_user.id
        # save User._id in session
        messages.success(request, 'Te has registrado exitosamente. ¡Ya puedes iniciar sesión!', extra_tags = 'registered')
        
        return redirect('/')

def login(request):
    username = request.POST["username"]
    password = request.POST["password"]
    print(f"{username} {password}")
    echeck = user.objects.filter(username=username) 
    print (echeck)
    if echeck:
        print('EXISTE USERNAME')
            #if echeck[0].password == password:
        if bcrypt.checkpw(request.POST['password'].encode(), echeck[0].password.encode()):
            print(echeck[0].password)
            request.session['login'] = True
            request.session['u_id'] = echeck[0].id
            return redirect('/dashboard')
        else:
            print('CONTRASEÑA INCORRECTA')
            messages.error(request,'Contraseña incorrecta', extra_tags = 'mal_login_pass_dato')
            return redirect('/')

    else: 
        messages.error(request,'Email No registrado', extra_tags = 'mal_dato_login_e')
        return redirect('/')

def dashboard(request):
    print('INGRESO AL DASHBOARD')
    if request.session['login'] == True:
        user_1 = user.objects.filter(id = request.session['u_id'])
        # user_info = {
        #     'user': user_1[0]
        # }
        # print(user_info['user'])
        context={
            'prueba': items.objects.all(),
            'user': user_1[0]
        }
        return render(request, 'Allitems.html', context)

    else:
        return redirect('/')

def addNewItem(request):
    context = {
        'more_item': items.objects.all()
    }
    return render(request, 'addNewitem.html', context)

def createItem(request):
    u = user.objects.get(id=request.session['u_id'])

    error_new = False
    print("*"*10)
    print(type(request.POST['title_in']))
    print("*"*10)

    if len(request.POST['title_in'])< 3:
        messages.error(request,'Tu Item debe tener al menos 2 carácteres.', extra_tags = 'title_error' )
        error_new = True
    if error_new == True:
        return redirect('/item/new')
    elif error_new == False:
        item_new=items.objects.create(nameItem=request.POST['title_in'], uploader = u)
        return redirect(f'/item/{item_new.id}')

def itemDetails(request,id):
    context={
        'item':items.objects.get(id=id)
    }
    var=context['item']
    print(f' item ==== {var.nameItem}')
    return render(request, 'itemDetails.html', context)


def deleteItem(request, id):
    item_d = items.objects.get(id=id)
    item_d.delete()
    return redirect('/dashboard')

def logout(request):
    request.session.clear()
    return redirect('/')

def quitItem(request, id):
    context={
        'item':items.objects.get(id=id)
    }
    return render(request, 'quitItem.html', context)