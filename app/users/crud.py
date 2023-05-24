
# class UserCrud:
#     def __init__(self, db: Session = Depends(get_db)):
#         self.db = db

#     def get_user(self, user_id: int):
#         return self.db.query(User).filter(User.id == user_id).first()

#     def get_user_by_email(self, email: str):
#         return self.db.query(User).filter(User.email == email).first()

#     def get_users(self, skip: int = 0, limit: int = 100):
#         return self.db.query(User).offset(skip).limit(limit).all()

#     def create_user(self, user: UserCreate):
#         fake_hashed_password = user.password + "notreallyhashed"
#         db_user = User(email=user.email, hashed_password=fake_hashed_password)
#         self.db.add(db_user)
#         self.db.commit()
#         self.db.refresh(db_user)
#         return db_user

#     def update_user(self, user_id: int, user: UserUpdate):
#         db_user = self.db.query(User).filter(User.id == user_id).first()
#         update_data = user.dict(exclude_unset=True)
#         for key, value in update_data.items():
#             setattr(db_user, key, value)
#         self.db.commit()
#         self.db.refresh(db_user)
#         return db_user

#     def delete_user(self, user_id: int):
#         db_user = self.db.query(User).filter(User.id == user_id).first()
#         self.db.delete(db_user)
#         self.db.commit()
#         return db_user


