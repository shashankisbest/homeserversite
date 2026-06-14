from django.shortcuts import render, redirect
from django.http import HttpResponse
from accounts.models import User

# Create your views here.



ALLOWED_STORAGE_ROOTS = {
    "server_storage" : "/home/SHASHANK1",
    "hdd1": "/mnt/old_hdd/hdd1",
    "hdd2": "/mnt/old_hdd/hdd2",
    "hdd3": "/mnt/old_hdd/hdd3",
}


def home(request):
    if 'user_id' not in request.session:
        return redirect('/')
    return render(request, "filetransfer/home.html", {
        "username": request.session['username'],
        "is_admin": request.session['is_admin']
    })


import os
from pathlib import PurePosixPath


def upload_files(request, root_name, subpath=None):

    files = request.FILES.getlist("files")

    upload_root = ALLOWED_STORAGE_ROOTS[root_name]
    if subpath:
        upload_root = os.path.join(upload_root, subpath)

    os.makedirs(upload_root, exist_ok=True)

    for uploaded_file in files:
        relative_path = PurePosixPath(uploaded_file.name.replace("\\", "/"))
        safe_parts = [part for part in relative_path.parts if part not in ("", ".", "..")]
        if not safe_parts:
            safe_parts = [os.path.basename(uploaded_file.name)]

        save_path = os.path.join(upload_root, *safe_parts)
        os.makedirs(os.path.dirname(save_path), exist_ok=True)

        with open(save_path, "wb+") as f:
            for chunk in uploaded_file.chunks():
                f.write(chunk)
    
    if subpath:
        return redirect(
            "upload_browse",
            root_name=root_name,
            subpath=subpath
        )

    return redirect(
        "upload_root",
        root_name=root_name
    )

def upload(request, root_name=None, subpath=None):


    if request.method == "POST":

        

        if request.POST.get("action") == "create_folder":

            folder_name = request.POST.get("new_folder_name")

            current_path = ALLOWED_STORAGE_ROOTS[root_name]

            if subpath:
                current_path = os.path.join(current_path, subpath)

            new_folder_path = os.path.join(
                current_path,
                folder_name
            )

            os.makedirs(
                new_folder_path,
                exist_ok=True
            )

            return redirect(request.path)



        return upload_files(request,root_name,subpath)

    
    # Home page of download explorer
    if root_name is None:
        return render(
            request,
            "filetransfer/upload.html",
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


        items.append({
            "name": item,
            "is_dir": os.path.isdir(full_path),
            "path": item_path,
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
        "filetransfer/upload.html",
        {
            "at_home": False,
            "root_name": root_name,
            "subpath": subpath,
            "items": items,
            "individual_paths": individual_paths,
        }
    )





def download(request, root_name=None, subpath=None):

    if request.method == "POST":

        if request.POST.get("action") == "create_folder":

            folder_name = request.POST.get("new_folder_name")

            current_path = ALLOWED_STORAGE_ROOTS[root_name]

            if subpath:
                current_path = os.path.join(current_path, subpath)

            new_folder_path = os.path.join(
                current_path,
                folder_name
            )

            os.makedirs(
                new_folder_path,
                exist_ok=True
            )

            return redirect(request.path)

            
    
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
    # Handle deletion of selected items
    if request.method == "POST":
        selected = request.POST.getlist("selected")
        if selected:
            cart = request.session.get("cart", [])
            # selected contains string indexes from the rendered list; remove in reverse order
            try:
                indices = sorted([int(i) for i in selected], reverse=True)
            except ValueError:
                indices = []

            for idx in indices:
                if 0 <= idx < len(cart):
                    cart.pop(idx)

            request.session["cart"] = cart
        return redirect(request.path)

    cart = request.session.get("cart", [])
    items = []
    for item in cart:
        name = os.path.basename(item["path"])
        items.append({
            "name": name,
            "path": os.path.join(item["root"], item["path"])
        })

    return render(request, "filetransfer/cart.html", {"items": items})


import zipfile
import tempfile
from django.http import FileResponse

def download_zip(request):
    cart = request.session.get("cart", [])
    # print("Downloading cart items:", cart)

    # return HttpResponse("This will trigger the download of a ZIP file containing the selected items.")

    if len(cart) == 0:
        return render(request, "filetransfer/cart.html", {
            "items": [],
            "error": "Your cart is empty. Please add items to the cart before downloading."
        })

    temp_file = tempfile.NamedTemporaryFile(
    dir="temp_zips",
    delete=False,
    suffix=".zip"
    )

    zip_path = temp_file.name
    temp_file.close()

    # creating zip file
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        
        for item in cart:

            root_path = ALLOWED_STORAGE_ROOTS[item["root"]]

            absolute_path = os.path.join(
                root_path,
                item["path"]
            )

            if os.path.isfile(absolute_path):

                zipf.write(
                    absolute_path,
                    arcname=os.path.basename(absolute_path)
                )

            elif os.path.isdir(absolute_path):

                for foldername, subfolders, filenames in os.walk(absolute_path):

                    for filename in filenames:

                        file_path = os.path.join(
                            foldername,
                            filename
                        )

                        arcname = os.path.relpath(
                            file_path,
                            os.path.dirname(absolute_path)
                        )

                        try:
                            zipf.write(
                                file_path,
                                arcname=arcname
                            )
                        except FileNotFoundError:
                            continue

    
    
    file_handle = open(zip_path, "rb")

    response = FileResponse(
        file_handle,
        as_attachment=True,
        filename="homeserver_download.zip"
    )


    return response






