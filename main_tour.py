from typing import List
from pydantic import BaseModel
from pymongo import MongoClient
from fastapi.encoders import jsonable_encoder
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
index = Jinja2Templates(directory="template1")
admin = Jinja2Templates(directory="template1")
login = Jinja2Templates(directory="template1")
home = Jinja2Templates(directory="template1")
admin_detials = Jinja2Templates(directory="template1")
book = Jinja2Templates(directory="template1")


uri = "mongodb+srv://demo:Demo_123@cluster0.6gozg1a.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri)
db = client.tourism


class User(BaseModel):
    user_name: str
    u_password: str

class Detail(BaseModel):
    place: str
    da_te: str
    days: int
    ph_no: int

@app.get("/loginPage", response_class=HTMLResponse)#http://127.0.0.1:8000/loginPage/
def show_login_page(request: Request):
    return login.TemplateResponse("login.html", context={"request": request})

@app.get("/registerPage", response_class=HTMLResponse)#http://127.0.0.1:8000/registerPage/
def show_login_page(request: Request):
    return index.TemplateResponse("L_index.html", context={"request": request})

@app.get("/homePage", response_class=HTMLResponse)#http://127.0.0.1:8000/homePage/
def home_page(request: Request):
    return home.TemplateResponse("home.html", context={"request": request})

@app.get("/bookPage", response_class=HTMLResponse)#http://127.0.0.1:8000/bookPage/
def book_page(request: Request):
    return book.TemplateResponse("book.html", context={"request": request})

@app.get("/adminPage", response_class=HTMLResponse)#http://127.0.0.1:8000/adminPage/
def admin_page(request: Request):
    return admin.TemplateResponse("admin.html", context={"request": request})

@app.get("/admin_details", response_class=HTMLResponse)#http://127.0.0.1:8000/admin_details/
def admin_page(request: Request):
    return admin_detials.TemplateResponse("admin_details.html", context={"request": request})

@app.post("/u_details", response_model=List[Detail])
def user_detail(detail: Detail,da_te = Form(),place = Form(),ph_no= Form(),days = Form()):
    detail = jsonable_encoder(detail)
    object_id = db["detail"].insert_one({"da_te": da_te})
    object_id = db["detail"].insert_one({"place": place})
    object_id = db["detail"].insert_one({"ph_no": ph_no})
    object_id = db["detail"].insert_one({"days": days})
    details = list(db["detail"].find(limit=100))
    return details

@app.post('/greet')#http://127.0.0.1:8000/greet/
def check_user(request: Request,username: str = Form(), upassword: str = Form()):
    '''
    checking username and password
    '''
    user = db["users"].find_one({"username": username})
    if username == "shruthi" and upassword == "shruthi@56" :
            return admin_detials.TemplateResponse("admin_details.html", context={"request": request})
    else:
        return "Unsuccessful sign_in"

@app.post("/processLogin")#http://127.0.0.1:8000/processLogin/
def check_user(request: Request, username: str = Form(), upassword: str = Form()):
    '''
    checking username and password
    '''
    user = db["users"].find_one({"username": username})
    if username == user["username"] and upassword == user["upassword"] :
        return home.TemplateResponse("home.html", context={"request": request})
    else:
        return "Unsuccessful sign_in"

class Information(BaseModel):
    uname: str
    udate: str
    udays: int
    places: str
    phone: int
    package: int

@app.get("/findAll",response_model=List[Information])#http://127.0.0.1:8000/findAll/
def list_users():
    informations = list(db["informations"].find(limit=100))
    return informations

@app.post("/book")#http://127.0.0.1:8000/book/
def book_users(response:Request,uname: str=Form(),udate: str=Form(),udays: int=Form(),
places: str=Form(),phone: int=Form(),package: int=Form()):
    information = {"uname":uname,"udate":udate,"udays":udays,"places":places,"phone":phone,"package":package}
    odject_id = db["informations"].insert_one(information)
    return "Booked Successfully"



@app.put("/update")#http://127.0.0.1:8000/update/
def update_users(phone: int, information: Information):
    information = jsonable_encoder(information)
    update_student = db["informations"].update_one({"phone": phone},{"$set": information})
    return f"{phone} updated successfully"

@app.delete("/delete")#http://127.0.0.1:8000/delete/
def delete_users(phone: int):
    delete_student = db["informations"].delete_one({"phone": phone})
    return f"{phone} delete successfully"

@app.post("/findOne")#http://127.0.0.1:8000/findOne/
def find_one(response:Request, phone: int=Form()):
    informations = db["informations"].find_one({"phone":phone})
    return informations


class Regsiter(BaseModel):
    name: str
    email: str
    da_te: str
    password: str
    phone: int

@app.post("/detail_register",)#http://127.0.0.1:8000/detail_register
def create_register(response:Request, name: str=Form(), email: str=Form(), da_te: str=Form(), password: str=Form(),phone: int=Form() ):
    tony={"name":name,"email":email,"da_te":da_te,"password":password,"phone":phone}
    object_id = db["regsiter"].insert_one(tony)
    return "Registered Successfully"
    #home.TemplateResponse("home.html", context={"response": Request})
