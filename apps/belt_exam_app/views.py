from django.shortcuts import render, redirect
from apps.belt_exam_app.models import User, Wishes
from django.contrib import messages
from django.contrib.messages import get_messages
import bcrypt


# Create your views here.


def index(request):

    return render(request, "belt_exam_app/index.html")




def login(request):


    matched_users = User.objects.filter(email=request.POST["email"])

    if matched_users:
        user = matched_users[0]

        pw_matched = bcrypt.checkpw(request.POST['password'].encode(),
                                    user.password.encode())

        if pw_matched:
            request.session['uid'] = user.id
        else:
            messages.error(request, "Invalid credentials")
            return redirect("/")
    else:
        messages.error(request, "Invalid credentials")
        messages.error(request, "Try again")
        return redirect("/")
    return redirect("/wishes")




def register(request):
    matched_users = User.objects.filter(email=request.POST["email"])

    if matched_users:
        return redirect("/")

    if request.POST["password"] != request.POST["password_confirm"]:
        messages.error(request, "Password must match confirm password")

    if len(request.POST["first_name"]) < 2:
        messages.error(request, "First Name must be at least 2 characters")

    storage = messages.get_messages(request)
    storage.used = False
    if len(storage) > 0:
        return redirect("/")
    # check if reg valid
    #if not User.objects.is_reg_valid(request):
        #return redirect ("/")

    hashed = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())

    new_user = User.objects.create(first_name=request.POST["first_name"], 
                                    last_name=request.POST["last_name"], 
                                    email=request.POST["email"], 
                                    password=hashed)

    #request.session["uid"] = new_user.id
    return redirect("/wishes")




def logout(request):
    request.session.clear()
    return redirect('/')




def wishes(request):
    uid = request.session.get("uid")

    if not uid:
        return redirect("/")

    user = User.objects.get(id=uid)
    context = {
        "uid": uid,
        "user": user,
        "this_users_wishes": user.created_wishes.filter(new_wish_field=False),
        "all_wishes_granted": Wishes.objects.filter(new_wish_field=True),
    }
    return render(request, "belt_exam_app/wishes.html", context)




def wishes_new(request):
    uid = request.session.get("uid")

    if not uid:
        return redirect("/")

    user = User.objects.get(id=uid)
    context = {
        "user": user,
    }
    return render(request, "belt_exam_app/wishes/new.html", context)




def wishes_create(request):
    uid = request.session.get("uid")

    if not request.session.get("uid"):
        return redirect("/")

    user = User.objects.get(id=uid)

    if len(request.POST["I wish for"]) < 3:
        messages.error(request, "A wish must consist of at least 3 characters!")
    
    if len(request.POST["Description"]) < 3:
        messages.error(request, "A description must consist of at least 3 characters!")

    if len(request.POST["I wish for"]) == 0:
        messages.error(request, "A wish must be provided!")
    
    if len(request.POST["Description"]) == 0:
        messages.error(request, "A description must be provided!")

    storage = messages.get_messages(request)
    storage.used = False
    if len(storage) > 0:
        return redirect("/wishes/new")

    new_wish = Wishes.objects.create(I_wish_for=request.POST["I wish for"], 
                                    wish_description=request.POST["Description"],
                                    created_by=user)
    
    return redirect("/wishes")




def remove(request, wish_id):

    wish_to_delete = Wishes.objects.get(id=wish_id)
    wish_to_delete.delete()

    return redirect(("/wishes"))




def edit_page(request, wish_id):

    wish_to_edit = Wishes.objects.get(id=wish_id)
    
    context = {
        "wish_to_edit": wish_to_edit,
    }
    
    return render(request, "belt_exam_app/edit.html", context)





def edit_process(request, id_wish_to_edit):
    
    uid = request.session.get("uid")

    if not request.session.get("uid"):
        return redirect("/")

    user = User.objects.get(id=uid)

    if len(request.POST["I wish for"]) < 3:
        messages.error(request, "A wish must consist of at least 3 characters!")
    
    if len(request.POST["Description"]) < 3:
        messages.error(request, "A description must consist of at least 3 characters!")

    if len(request.POST["I wish for"]) == 0:
        messages.error(request, "A wish must be provided!")
    
    if len(request.POST["Description"]) == 0:
        messages.error(request, "A description must be provided!")

    storage = messages.get_messages(request)
    storage.used = False
    if len(storage) > 0:
        return redirect("/wishes/edit/{{ wish_to_edit.id }}")

    wish_to_edit = Wishes.objects.get(id=id_wish_to_edit)

    wish_to_edit.I_wish_for = request.POST["I wish for"]
    wish_to_edit.wish_description = request.POST["Description"]

    wish_to_edit.save()
    
    return redirect("/wishes")




def granted(request, wish_id):

    wish_to_grant = Wishes.objects.get(id=wish_id)
    
    wish_to_grant.new_wish_field = True
    wish_to_grant.save()

    return redirect("/wishes")




def likes(request, wish_id):
    uid = request.session.get("uid")

    if not uid:
        return redirect("/")
    
    user = User.objects.get(id=uid)
    wish = Wishes.objects.filter(id=wish_id).first()

    if wish is not None:

        if user in wish.likers.all():
            wish.likers.remove(user)
        else:
            wish.likers.add(user)

    return redirect("/wishes")



def stats(request):

    uid = request.session.get("uid")

    if not uid:
        return redirect("/")
    
    user = User.objects.get(id=uid)
    context = {
        "user": user,
        "granted_wishes_all_users": Wishes.objects.filter(new_wish_field=True),
        "users_granted_wishes": user.created_wishes.filter(new_wish_field=True),
        "users_wishlist": user.created_wishes.filter(new_wish_field=False),
    }

    return render(request, "belt_exam_app/stats.html", context)