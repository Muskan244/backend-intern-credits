from sqlalchemy.orm import DeclarativeBase, relationship, Mapped, mapped_column
from sqlalchemy import Integer, String, ForeignKey, DateTime, func

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email:   Mapped[str] = mapped_column(String, unique=True, nullable=False)
    name:    Mapped[str] = mapped_column(String, nullable=False)

    credit:  Mapped["Credit"] = relationship(back_populates="user", uselist=False)

class Credit(Base):
    __tablename__ = "credits"

    user_id:      Mapped[int] = mapped_column(ForeignKey("users.user_id", ondelete="CASCADE"), primary_key=True)
    credits:      Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    last_updated: Mapped["DateTime"] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())

    user: Mapped[User] = relationship(back_populates="credit")
