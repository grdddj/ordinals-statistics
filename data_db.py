from sqlalchemy import (
    Column,
    Engine,
    Index,
    Integer,
    String,
    UniqueConstraint,
    create_engine,
)
from sqlalchemy.orm import Query, Session, declarative_base, sessionmaker

# db_location = "example.db"
db_location = "/mnt/bitcoin2/ord_data/ord_data.db"


def get_session() -> Session:
    engine = get_engine()
    return sessionmaker(bind=engine)()


def get_engine() -> Engine:
    return create_engine(f"sqlite:///{db_location}", echo=False)


def get_query() -> Query:
    session = get_session()
    return session.query(InscriptionModel)


# Define the base class for database models
Base = declarative_base()


class InscriptionModel(Base):
    __tablename__ = "inscriptions"

    id = Column(Integer, primary_key=True)
    tx_id = Column(String, nullable=False)
    minted_address = Column(String, nullable=False)
    content_type = Column(String, nullable=False)
    content_hash = Column(String, nullable=False)
    datetime = Column(String, nullable=False)
    timestamp = Column(Integer, nullable=False)
    content_length = Column(Integer, nullable=False)
    genesis_fee = Column(Integer, nullable=False)
    genesis_height = Column(Integer, nullable=False)
    output_value = Column(Integer, nullable=False)
    sat_index = Column(Integer, nullable=False)

    __table_args__ = (
        UniqueConstraint("tx_id", name="uq_tx_id"),  # secondary key to tx_id
        Index("ix_inscriptions_id", "id", unique=True),  # for bulk inserts to work
    )

    def __repr__(self):
        return f"<Inscription({self.id}, {self.tx_id}, {self.content_type}, {self.content_length:_})>"


if __name__ == "__main__":
    # Create the table in the database
    Base.metadata.create_all(get_engine())
