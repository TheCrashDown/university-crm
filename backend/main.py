from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers.quiz_router import router as quiz_router
from routers.teacher_router import router as teacher_router
from routers.student_router import router as student_router
from routers.admin_router import router as admin_router
from routers.auth_router import router as auth_router
from routers.chat_router import router as chat_router
from routers.test_router import router as test_router

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(quiz_router, prefix="/quiz", tags=["Working with quizes"])
app.include_router(teacher_router, prefix="/teacher", tags=["Teacher functions"])
app.include_router(student_router, prefix="/student", tags=["Student functions"])
app.include_router(admin_router, prefix="/admin", tags=["Admin & debug functions"])
app.include_router(auth_router, prefix="/auth", tags=["Auth functions"])
app.include_router(chat_router, prefix="/chat", tags=["Chat functions"])
app.include_router(test_router, prefix="/test", tags=["Test functions"])
