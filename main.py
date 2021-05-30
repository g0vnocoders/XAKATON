from typing import List

from fastapi import Depends, FastAPI, HTTPException,Response, Form
from sqlalchemy.orm import Session
import random
from sqlalchemy.sql.expression import true
from starlette.responses import FileResponse, HTMLResponse, RedirectResponse

from fastapi.staticfiles import StaticFiles
import crud, models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/",response_class=RedirectResponse)
async def mainpage():
    return RedirectResponse("landing.html")


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Електронна скринька вже зареєстрована")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Користувача не знайдено!")
    return db_user


@app.post("/users/{user_password}/items/", response_model=schemas.Item)
def create_item_for_user(
    user_password: str, item: schemas.ItemCreate, db: Session = Depends(get_db)
):
    return crud.create_user_item(db=db, item=item, user_password=user_password)


@app.get("/items/", response_model=List[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items

@app.delete("/items/",)
def delete_item(id:str, db: Session = Depends(get_db)):
    items = crud.delete_item_by_id(db, id=id)
    return True


@app.post("/auth",response_class=HTMLResponse)
def auth_user(password:str=Form(...)):
    response=HTMLResponse("<script>window.location.href='/admin.html'</script>")
    response.set_cookie(key="password", value=password)#НЕ РОБІТЬ ТАК НА ПРОДІ
    return response                                    #ГЕНЕРУЙТЕ ТОКЕНИ ТА ПРИВʼЯЗУЙТЕ ЇХ




#FAKE
def getdate():
    return str(random.randint(10,19))+":"+str(random.choice(["00","05",10,15,20,25,30,35,40,45,50,55]))

shit=[
    ["Кафедра","Курси","Факультет","Гурток","Секція"],
    ["спорту","конструювання","малювання","танців","моделювання","Англійської мови",
    "Китайської мови","Програмування","Лайнокодингу","Медицини","Карате","Turbo Pascal"],
    ["Павлов","Порошенко","Янукович","Лінус","Путін","Білл","Стів","Балашов","Шалун","Дзюба","Черніков","Тимошенко",
    "Лукашенко","Якубович","Гітлер","Шкарлет"],
    ["Артем","Олександр","Віктор","Торвальдс","Володимир","Гейтс","Джобс","Геннадій","Максим","Марк","Олег","Ілля"],
    ["Артемович","Олександрович","Вікторович","Торвальдсович","Володимирович","Гейтсович","Джобсович",
    "Геннадієвич","Максимович","Маркович"]
]

def gettopic():
    return random.choice(shit[0])+" "+random.choice(shit[1])

def getname():
    return random.choice(shit[2])+" "+random.choice(shit[3])+" "+random.choice(shit[4])

@app.get("/fakeitems/", response_model=List[schemas.Item])
def read_itemssus(skip: int = 0, limit: int = 100):
    topics=["1","2"]
    items=[]
    items.append(schemas.Item(title=gettopic(),description="",start=getdate(),end=getdate(),days=127,id=123,owner_name=getname(),name=getname(),type="Integer"))
    
    items.append(schemas.Item(title=gettopic(),description="",start=getdate(),end=getdate(),days=31,id=123,owner_name=getname(),name=getname(),type="Integer"))
    
    for days in reversed(range(2,128)):
        items.append(schemas.Item(title=gettopic(),description="",start=getdate(),end=getdate(),days=days,id=123,owner_name=getname(),name=getname(),type="Integer"))
    return items

app.mount("/", StaticFiles(directory="."), name="static")    