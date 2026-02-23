from app.database import SessionLocal, engine
from app.models.user import User
from app.database import Base

Base.metadata.create_all(bind=engine)

db = SessionLocal()

admin_email = "admin@camcoach.com"
admin = db.query(User).filter(User.email == admin_email).first()

if not admin:
    hashed = User.hash_password("Bogota2025@")  # la contrasena aqui
    new_admin = User(
        email=admin_email,
        hashed_password=hashed,
        rol="admin",
        is_active=True
    )
    db.add(new_admin)
    db.commit()
    print("Administrador creado exitosamente!")
else:
    print("El administrador ya existe.")

db.close()