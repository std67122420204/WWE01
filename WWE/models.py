from WWE.extensions import db, login_manager
from sqlalchemy import Integer, String, Text, Table, Column, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from datetime import datetime
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    if user_id:
        return db.session.get(User, int(user_id))
    return None


class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(100), nullable=False)

    firstname: Mapped[str] = mapped_column(String(30), nullable=True)
    lastname: Mapped[str] = mapped_column(String(30), nullable=True)
    avatar: Mapped[str] = mapped_column(String(25), default='avatar.png')

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

  
    wwes: Mapped[List['WWE']] = relationship(back_populates='user')

    def __repr__(self):
        return f'<User: {self.username}>'


wwe_type = Table(
    'wwe_type',
    db.metadata,
    Column('type_id', Integer, ForeignKey('type.id'), primary_key=True),
    Column('wwe_id', Integer, ForeignKey('wwe.id'), primary_key=True)
)


class Type(db.Model):
    __tablename__ = 'type'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)

   
    wwes: Mapped[List['WWE']] = relationship(
        back_populates='categories', 
        secondary=wwe_type
    )

    def __repr__(self):
        return f'<Type: {self.name}>'


class WWE(db.Model):
    __tablename__ = 'wwe'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    height: Mapped[str] = mapped_column(String(20), nullable=False)
    weight: Mapped[str] = mapped_column(String(20), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    img_url: Mapped[str] = mapped_column(Text, nullable=False)

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'))

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    
    user: Mapped['User'] = relationship(back_populates='wwes')

    categories: Mapped[List['Type']] = relationship(
        back_populates='wwes',      
        secondary=wwe_type
    )

    def __repr__(self):
        return f'<WWE: {self.name}>'