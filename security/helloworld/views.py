from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
import datetime
import pyrebase
import json

# Create your views here.
config = {
    'apiKey': "AIzaSyD7H6ZxUcR0M9acTTrg7cyV0Dxu4C27cUU",
    'authDomain': "security-sgp.firebaseapp.com",
    'databaseURL': "https://security-sgp.firebaseio.com",
    'projectId': "security-sgp",
    'storageBucket': "security-sgp.appspot.com",
    'messagingSenderId': "193607441095",
    'appId': "1:193607441095:web:5ce212a4b4e7228c7efce2",
    'measurementId': "G-LDXTDF1K5V"
    # 'apiKey': "AIzaSyBplgfDMaVZSDahuI2RwF24a7e2K4vVXcs",
    # 'authDomain': "videobase-dynamic-auth-system.firebaseapp.com",
    # 'databaseURL': "https://videobase-dynamic-auth-system.firebaseio.com",
    # 'projectId': "videobase-dynamic-auth-system",
    # 'storageBucket': "videobase-dynamic-auth-system.appspot.com",
    # 'messagingSenderId': "542414051699",
    # 'appId': "1:542414051699:web:4625898e615fba4dc88d06"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()
auth = firebase.auth()
authToken = ""
uname = ""


def signIn(request):
    return render(request, "signIn.html")


def index(request):
    return render(request, "index.html")


def homePage(request):
    if authToken != "":
        return render(request, "screen.html")
    else:
        messages.info(request, 'Please SignIn')
        return render(request, 'signIn.html')


def postsign(request):
    global uname
    uname = request.POST['email']
    passw = request.POST['pass']
    global authToken
    # db.child('users').child(uname).set(data)
    # i = db.child('image').child('img').get()
   # i = "https://firebasestorage.googleapis.com/v0/b/security-sgp.appspot.com/o/images%2Fdemo.jpg?alt=media&token=b887b2c7-a21e-4a64-a20d-043515578392"
    try:
        user = auth.sign_in_with_email_and_password(uname, passw)
        # print(user)
        authToken = auth.current_user.get('localId')
    except:
        messages.info(request, 'Invalid Credentials')
        return render(request, 'signIn.html')

    return render(request, "firstPage.html")


def logout(request):
    global authToken
    authToken = ""
    return render(request, "signIn.html")


def get_logs_db():
    x = datetime.datetime.now()
    date = x.strftime("%m") + "-" + x.strftime("%d") + "-" + x.strftime("%Y")
    i = db.child("01-28-2020").get()
    return i


def get_log(request):
    results = get_logs_db()
    # print(results.val())
    user1 = {}
    for users in results.each():
        # {name": "Mortimer 'Morty' Smith"}
        # key.append(str(user.key()) + )
        # val.append(str(user.val()))
        user1[str(users.key())] = str(users.val())

    if user1 == {}:
        return []
    user1 = json.dumps(user1)
    return JsonResponse(user1, safe=False)


def addPerson(request):
    print("Called")
    if request.method == 'POST':
        name = request.POST['name']
        mno = request.POST['mno']
        designation = request.POST['designation']
        pEmp = request.POST['pEmp']
        duration = request.POST['duration']
        date = str(datetime.datetime.now())
        if pEmp == True:
            data = {
                'Name': name,
                'Contact No': mno,
                'Designation': designation,
                'RegisteredBy': uname,
                'RegisteredOn': date,
                'Permenant Employee': pEmp
            }
        else:
            data = {
                'Name': name,
                'Contact No': mno,
                'Designation': designation,
                'Permenant Employee': pEmp,
                'RegisteredBy': uname,
                'RegisteredOn': date,
                'duration': duration
            }

        db.child('RegisteredPerson').child(mno).set(data)

    return HttpResponse("<h1>form submitted</h1>")