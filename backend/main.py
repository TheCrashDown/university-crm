from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers.polls_router import router as polls_router
from routers.teacher_router import router as teacher_router
from routers.student_router import router as student_router

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(polls_router, prefix="/polls", tags=["Working with polls"])
app.include_router(teacher_router, prefix="/teacher", tags=["Student functions"])
app.include_router(student_router, prefix="/student", tags=["Teacher functions"])
