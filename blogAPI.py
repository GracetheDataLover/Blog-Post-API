from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from uuid import UUID, uuid4
from typing import List, Optional

app = FastAPI()

class Post(BaseModel):
    id: Optional[UUID] = None
    title: str
    body: str
    author: Optional[str]
    published: bool = False

blog = []

@app.post("/blog", response_model=Post)
def create_post(post: Post):
    post.id = uuid4()
    blog.append(post)
    return post

@app.get("/blog", response_model=List[Post])
def read_posts():
    return blog

@app.get("/blog/{post_id}", response_model=Post)
def read_post(post_id: UUID):
    for post in blog:
        if post.id == post_id:
            return post
    
    raise HTTPException(status_code=404, detail="Task not found")

@app.put("/blog/{post_id}", response_model=Post)
def update_post(post_id: UUID, post_update: Post):
    for idx, post in enumerate(blog):
        if post.id == post_id:
            updated_post = post.copy(update=post_update.dict(exclude_unset=True))
            blog[idx] = updated_post
            return updated_post
    
    raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/blog/{post_id}", response_model=Post)
def delete_post(post_id: UUID):
    for idx, post in enumerate(blog):
        if post.id == post_id:
            return blog.pop(idx) # Removes the post at position "idx"(index) from the "blog" list and returns that deleted post as the API response
        
    raise HTTPException(status_code=404, detail="Task not found")

if __name__ == "__main__":
    import uvicorn

# Let's run this

    uvicorn.run("blogAPI:app", host="127.0.0.1", port=8001)


#run this up now
