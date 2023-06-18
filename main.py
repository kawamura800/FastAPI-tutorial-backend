# URLと対応する処理をするためのファイル
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

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


origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def Hello():
    return {"Hello": "World!"}


# @app.post("/users/", response_model=schemas.User)
# def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
#     db_user = crud.get_user_by_email(db, email=user.email)
#     if db_user:
#         raise HTTPException(status_code=400, detail="Email already registered")
#     return crud.create_user(db=db, user=user)


# @app.get("/users/", response_model=list[schemas.User])
# def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     users = crud.get_users(db, skip=skip, limit=limit)
#     return users


# @app.get("/users/{user_id}", response_model=schemas.User)
# def read_user(user_id: int, db: Session = Depends(get_db)):
#     db_user = crud.get_user(db, user_id=user_id)
#     if db_user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return db_user


# @app.post("/users/{user_id}/tasks/", response_model=schemas.Todo)
# def create_task_for_user(
#     user_id: int, task: schemas.TaskCreate, db: Session = Depends(get_db)
# ):
#     return crud.create_user_task(db=db, task=task, user_id=user_id)


# Todoの一覧表示
@app.get("/todos/", response_model=list[schemas.Todo])
def read_todos(limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_todos(db, limit=limit)


# Todoの追加
@app.post("/todos/", response_model=schemas.Todo)
async def add_todo(todo: schemas.TodoCreate, db: Session = Depends(get_db)):
    return crud.create_todo(db, todo)


# Todoの編集
@app.put("/todos/{todo_id}")
async def edit_todo(todo_id: int, db: Session = Depends(get_db)):
    return crud.update_todo(db, todo_id)


# Todoの削除
@app.delete("/todos/{todo_id}")
async def remove_todo(todo_id: int, db: Session = Depends(get_db)):
    return crud.delete_todo(db, todo_id)
