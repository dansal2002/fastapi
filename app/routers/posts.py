from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, oauth2
from ..database import engine, get_db
from sqlalchemy.orm import Session
from typing import List, Optional
from sqlalchemy import func

router = APIRouter(
    prefix="/posts", # removed /posts from router.post("/post")
    tags=['Posts']
)

@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str]= ""):
   # cursor.execute("""SELECT * FROM POSTS""" ) #RAW SQL methods
  #  posts = cursor.fetchall()
   # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all() ##filters added to end of "posts" below
   # GET ONLY YOUR POSTS : posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()

    #SQL Query RAW = SELECT posts.*, COUNT(votes.post_id) as votes FROM posts LEFT JOIN votes ON posts.id = votes.post_id group by posts.id;
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    return posts

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
  #  cursor.execute("""INSERT INTO posts (title,content,published) VALUES (%s, %s, %s) RETURNING *""", (post.title, post.content, post.published)) # %s is a variable for santization, second arg passes data in order to %s's   
  #  new_post = cursor.fetchone()
  #  conn.commit() #pushes to DB
  #**post.dict() #** unpacks a dictionary
  #  # new_post = models.Post(title=post.title, content=post.content, published=post.published) # Below is the better way to do it with unpacking a dict
  new_post = models.Post(owner_id=current_user.id, **post.dict())
  db.add(new_post) #store it
  db.commit() #commit it
  db.refresh(new_post) # store it back into new_post to replace RETURNING in SQL
  return new_post


@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)): #converts to int
    #cursor.execute("""SELECT * FROM posts WHERE id = %s""",(str(id),))
   # post=cursor.fetchone()
 #  post = db.query(models.Post).filter(models.Post.id == id).first() # finds only first instance
   post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()

   if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")
   return post

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)): 
    #cursor.execute("""DELETE FROM posts WHERE id = %s returning *""", (str(id),))
    #deleted_post=cursor.fetchone()
    #conn.commit() #apply change
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete")

    post_query.delete(synchronize_session=False)

    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.Post)
def updatepost(id:int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)): #converts to int
   # cursor.execute("""UPDATE posts SET title = %s, content = %s, published =%s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, str(id)),)
   # updated_post=cursor.fetchone()
   # conn.commit() #apply change
   # index=find_index_post(id)
   post_query = db.query(models.Post).filter(models.Post.id == id)
   post = post_query.first()
   if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"post with id: {id} does not exist")

   if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update")

   post_query.update(updated_post.dict(),synchronize_session=False)
   db.commit()
   return post_query.first()