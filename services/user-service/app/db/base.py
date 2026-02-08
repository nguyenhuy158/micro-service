from sqlalchemy.orm import DeclarativeBase, declared_attr


class Base(DeclarativeBase):
    # Generate __tablename__ automatically
    @declared_attr.directive
    def __tablename__(self) -> str:
        return self.__name__.lower() + "s"
