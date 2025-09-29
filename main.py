from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.lawyer.registration1 import lawyer_registration1_router
from api.lawyer.registration2 import lawyer_registration2_router
from api.lawyer.registration3 import lawyer_registration3_router
from api.lawyer.registration4 import lawyer_registration4_router
from api.lawyer.registration5 import lawyer_registration5_router
from api.lawyer.registration6 import lawyer_registration6_router
from api.lawyer.getlawyerfulldetails import get_all_router



from api.lawyer.excelupload import excel_router



from api.user.user import user_router
from api.user.auth import auth_router



from api.admin.admin import admin_router

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI

app = FastAPI(
    title="Lexfactos Backend",
    description="FastAPI backend with Lawyer Registration & AWS S3 integration",
    version="1.0.0"
)

# CORS settings
origins = [
    "https://lexfactos-frontend.onrender.com",
    "http://localhost:3000",  # for local testing
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,        # Only allow your frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



app.include_router(lawyer_registration1_router)
app.include_router(lawyer_registration2_router)
app.include_router(lawyer_registration3_router)
app.include_router(lawyer_registration4_router)
app.include_router(lawyer_registration5_router)
app.include_router(lawyer_registration6_router)



app.include_router(user_router)
app.include_router(auth_router)



app.include_router(admin_router)



app.include_router(get_all_router)


app.include_router(excel_router)

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the Lexfactos Backend 🚀"}

# Health check
@app.get("/health")
def health_check():
    return {"status": "ok"}

# Example: Dummy route
@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {
        "item_id": item_id,
        "query": q,
        "detail": "This is a dummy item response"
    }

# Run: uvicorn main:app --reload
