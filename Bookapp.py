from typing import Optional
from fastapi import FastAPI, Body, Path, Query, HTTPException
from pydantic import BaseModel, Field
from starlette import status
import uvicorn
import threading
import requests
import streamlit as st

# -------------------- FASTAPI BACKEND --------------------
app = FastAPI()


class Book:
    def __init__(self, id: int, title: str, author: str, desc: str, rating: int):
        self.id = id
        self.title = title
        self.author = author
        self.desc = desc
        self.rating = rating


class BookModel(BaseModel):
    id: Optional[int] = Field(default=None, description="id is not needed to create")
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    desc: str = Field(min_length=3)
    rating: int = Field(gt=0, lt=6)

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "a new book",
                "author": "codewithmik",
                "desc": "great learning",
                "rating": 5,
            }
        }
    }


Books = [
    Book(1, "start with py", "yc", "amzing book", 5),
    Book(2, "start with fsapi", "jc", "interesting", 5),
    Book(3, "start with endpoints", "kc", "splendid", 5),
    Book(4, "start with jq", "yc", "not good", 3),
    Book(5, "start with rust", "yc", "not good", 2),
    Book(6, "start with d", "yc", "not good", 1),
]


@app.get("/books", status_code=status.HTTP_202_ACCEPTED)
async def read_all_books():
    return Books


@app.post("/create_book", status_code=status.HTTP_201_CREATED)
async def create_book(book_request: BookModel):
    new_book = Book(**book_request.model_dump())
    Books.append(find_book_id(new_book))
    return {"message": "Book created", "book": new_book.__dict__}


@app.get("/book/{book_id}", status_code=status.HTTP_200_OK)
async def find_book_by_id(book_id: int = Path(gt=0)):
    for b in Books:
        if b.id == book_id:
            return b
    raise HTTPException(status_code=404, detail="Book not found")


@app.get("/book/")
async def read_book_by_rating(book_rating: int = Query(lt=6, gt=0)):
    book_return = [b for b in Books if b.rating == book_rating]
    return book_return


def find_book_id(book: Book):
    book.id = 1 if len(Books) == 0 else Books[-1].id + 1
    return book


@app.put("/book/update_book", status_code=status.HTTP_200_OK)
async def update_book_by_id(book: BookModel):
    for i in range(len(Books)):
        if Books[i].id == book.id:
            Books[i] = book
            return {"message": "Book updated"}
    raise HTTPException(status_code=404, detail="not found")


@app.delete("/books/{book_id}", status_code=status.HTTP_200_OK)
async def delete_book(book_id: int):
    for i in range(len(Books)):
        if Books[i].id == book_id:
            Books.pop(i)
            return {"message": "Book deleted"}
    raise HTTPException(status_code=404, detail="not found")


# -------------------- STREAMLIT FRONTEND --------------------

FASTAPI_URL = "http://127.0.0.1:8000"


def run_fastapi():
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="error")


# Start FastAPI in background thread
threading.Thread(target=run_fastapi, daemon=True).start()

st.title("📚 Book Manager (FastAPI + Streamlit)")

menu = st.sidebar.selectbox("Menu", ["View Books", "Add Book", "Search by ID", "Search by Rating", "Update Book", "Delete Book"])

if menu == "View Books":
    if st.button("Load All Books"):
        res = requests.get(f"{FASTAPI_URL}/books")
        if res.status_code == 202:
            st.json(res.json())

elif menu == "Add Book":
    with st.form("add_book"):
        title = st.text_input("Title")
        author = st.text_input("Author")
        desc = st.text_area("Description")
        rating = st.number_input("Rating", min_value=1, max_value=5, step=1)
        submitted = st.form_submit_button("Add Book")
        if submitted:
            res = requests.post(f"{FASTAPI_URL}/create_book", json={
                "title": title, "author": author, "desc": desc, "rating": rating
            })
            st.success(res.json())

elif menu == "Search by ID":
    book_id = st.number_input("Book ID", min_value=1, step=1)
    if st.button("Find Book"):
        res = requests.get(f"{FASTAPI_URL}/book/{book_id}")
        if res.status_code == 200:
            st.json(res.json())
        else:
            st.error("Book not found")

elif menu == "Search by Rating":
    rating = st.number_input("Rating", min_value=1, max_value=5, step=1)
    if st.button("Find Books"):
        res = requests.get(f"{FASTAPI_URL}/book/", params={"book_rating": rating})
        st.json(res.json())

elif menu == "Update Book":
    with st.form("update_book"):
        book_id = st.number_input("Book ID", min_value=1, step=1)
        title = st.text_input("New Title")
        author = st.text_input("New Author")
        desc = st.text_area("New Description")
        rating = st.number_input("New Rating", min_value=1, max_value=5, step=1)
        submitted = st.form_submit_button("Update")
        if submitted:
            res = requests.put(f"{FASTAPI_URL}/book/update_book", json={
                "id": book_id, "title": title, "author": author, "desc": desc, "rating": rating
            })
            if res.status_code == 200:
                st.success(res.json())
            else:
                st.error("Book not found")

elif menu == "Delete Book":
    book_id = st.number_input("Book ID to delete", min_value=1, step=1)
    if st.button("Delete"):
        res = requests.delete(f"{FASTAPI_URL}/books/{book_id}")
        if res.status_code == 200:
            st.success(res.json())
        else:
            st.error("Book not found")
