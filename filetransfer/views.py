from django.shortcuts import render, redirect
from django.http import HttpResponse
from accounts.models import User

# Create your views here.



ALLOWED_STORAGE_ROOTS = {
    "server_storage" : "/home/SHASHANK1"
}


def home(request):
    if 'user_id' not in request.session:
        return redirect('/')
    return render(request, "filetransfer/home.html", {
        "username": request.session['username'],
        "is_admin": request.session['is_admin']
    })


def upload(request):
    return render(request, "filetransfer/upload.html")

import os



def download(request, root_name=None, subpath=None):
    
    if "cart" not in request.session:
        request.session["cart"] = []

    cart = request.session.get("cart", [])

    cart_count = len(cart)
    print(request.session["cart"])

    # Home page of download explorer
    if root_name is None:
        return render(
            request,
            "filetransfer/download.html",
            {
                "at_home": True,
                "roots": ALLOWED_STORAGE_ROOTS.keys()
            }
        )

    root_path = ALLOWED_STORAGE_ROOTS[root_name]

    current_path = root_path

    if subpath:
        current_path = os.path.join(root_path, subpath)

    items = []

    for item in os.listdir(current_path):

        full_path = os.path.join(current_path, item)

        if subpath:
            item_path = os.path.join(subpath, item)
        else:
            item_path = item

        selected = any(
            x["root"] == root_name and
            x["path"] == item_path
            for x in cart
        )

        items.append({
            "name": item,
            "is_dir": os.path.isdir(full_path),
            "path": item_path,
            "selected": selected,
        })

    items.sort(
        key=lambda x: (not x["is_dir"], x["name"].lower())
    )


    #setting up breadcrumbs
    individual_paths = []

    if subpath:

        path_parts = subpath.split(os.sep)

        for i in range(len(path_parts)):

            part_path = os.sep.join(path_parts[:i+1])

            individual_paths.append({
                "name": path_parts[i],
                "path": part_path
            })



    return render(
        request,
        "filetransfer/download.html",
        {
            "at_home": False,
            "root_name": root_name,
            "subpath": subpath,
            "items": items,
            "individual_paths": individual_paths,
            "cart_count": cart_count
        }
    )

def toggle_selection(request): #this view just adds or removes items from the cart in currnet session

    root_name = request.GET.get("root")
    item_path = request.GET.get("path")

    cart = request.session.get("cart", [])

    exists = False

    for item in cart:
        if item["root"] == root_name and item["path"] == item_path:
            exists = True
            break

    if exists:
        cart = [
            item
            for item in cart
            if not (
                item["root"] == root_name and
                item["path"] == item_path
            )
        ]
    else:
        cart.append({
            "root": root_name,
            "path": item_path
        })

    request.session["cart"] = cart

    return redirect(request.META.get("HTTP_REFERER", "/"))


def cart(request):
    
    cart = request.session.get("cart", [])
    items = []
    for item in cart:
        name = os.path.basename(item["path"])
        items.append({
            "name": name,
            "path": os.path.join(item["root"], item["path"])
        })
    return render(request, "filetransfer/cart.html", {"items": items})