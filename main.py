from fastapi import FastAPI

from routes import corpus, types, users, files

import uvicorn

app = FastAPI()


#routers
app.include_router(corpus.corpus_router, prefix='/corpus')
app.include_router(types.type_router, prefix='/type')
app.include_router(users.user_router, prefix='/user')
app.include_router(files.file_router, prefix='/file')

if __name__ == "__main__":
    uvicorn.run("main:app",host="127.0.0.1",port=8000,reload=True)
