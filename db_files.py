from sqlalchemy import Column, Engine, Index, LargeBinary, String, create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

# db_location = "example.db"
db_location = "/mnt/bitcoin2/ord_data/ord_content_data.db"


def get_session() -> Session:
    engine = get_engine()
    return sessionmaker(bind=engine)()


def get_engine() -> Engine:
    return create_engine(f"sqlite:///{db_location}", echo=False)


# Define the base class for database models
Base = declarative_base()


# Define the model for the byte data table
class ByteData(Base):
    __tablename__ = "byte_data"
    id = Column(String, primary_key=True)
    data = Column(LargeBinary)
    __table_args__ = (
        Index("ix_byte_data_id", "id", unique=True),
    )  # for bulk inserts to work


if __name__ == "__main__":
    # Create the table in the database
    Base.metadata.create_all(get_engine())
