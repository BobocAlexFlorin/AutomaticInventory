import sqlalchemy as sa
from .database import Base


class User(Base):
__tablename__ = 'Users'
Id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
Name = sa.Column(sa.NVARCHAR(100), nullable=False)
Department = sa.Column(sa.NVARCHAR(100))
Email = sa.Column(sa.NVARCHAR(100), unique=True)


class Category(Base):
__tablename__ = 'Categories'
Id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
Name = sa.Column(sa.NVARCHAR(100), unique=True, nullable=False)
Description = sa.Column(sa.NVARCHAR)


class Device(Base):
__tablename__ = 'Devices'
Id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
SerialNumber = sa.Column(sa.NVARCHAR(100), unique=True, nullable=False)
Vendor = sa.Column(sa.NVARCHAR(100))
Model = sa.Column(sa.NVARCHAR(100))
CategoryId = sa.Column(sa.Integer, sa.ForeignKey('Categories.Id', ondelete='SET NULL'))
UserId = sa.Column(sa.Integer, sa.ForeignKey('Users.Id', ondelete='CASCADE'))
DateAdded = sa.Column(sa.DateTime, server_default=sa.func.sysdatetime())