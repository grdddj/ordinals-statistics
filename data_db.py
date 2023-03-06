from typing import Iterator, Self

from sqlalchemy import (
    Column,
    Engine,
    ForeignKey,
    Index,
    Integer,
    String,
    UniqueConstraint,
    create_engine,
)
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Session, declarative_base, relationship, sessionmaker

db_location = "/mnt/bitcoin2/ord_data/ord_data.db"


def get_session() -> Session:
    engine = get_engine()
    return sessionmaker(bind=engine)()


def get_engine() -> Engine:
    return create_engine(f"sqlite:///{db_location}", echo=False)


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
    collection_id = Column(String, ForeignKey("inscriptions_collections.id"))
    collection = relationship("CollectionModel", back_populates="inscriptions")
    name_from_collection = Column(String)

    # TODO: is_in_collection(self) -> bool

    __table_args__ = (
        UniqueConstraint("tx_id", name="uq_tx_id"),  # secondary key to tx_id
        Index("ix_inscriptions_id", "id", unique=True),  # for bulk inserts to work
    )

    def __repr__(self) -> str:
        return f"<Inscription({self.id}, {self.tx_id}, {self.content_type}, {self.content_length:_})>"

    def tx_id_ellipsis(self) -> str:
        return f"{self.tx_id[:4]}...{self.tx_id[-4:]}"

    def ordinals_com_link(self) -> str:
        return f"https://ordinals.com/inscription/{self.tx_id}i0"

    def mempool_space_link(self) -> str:
        return f"https://mempool.space/tx/{self.tx_id}"

    @classmethod
    def by_tx_id(cls, tx_id: str) -> Self:
        session = get_session()
        return (
            session.query(InscriptionModel)
            .filter(InscriptionModel.tx_id == tx_id)
            .first()
        )


class CollectionModel(Base):
    __tablename__ = "inscriptions_collections"

    id = Column(String, primary_key=True)
    name = Column(String)
    inscription_icon = Column(String)
    supply = Column(String)
    slug = Column(String)
    description = Column(String)
    twitter_link = Column(String)
    discord_link = Column(String)
    website_link = Column(String)
    inscriptions = relationship("InscriptionModel", back_populates="collection")

    def __repr__(self) -> str:
        return (
            f"<Collection({self.id}, {self.name}, {self.supply}, {self.description})>"
        )

    def link_ordinalswallet(self) -> str:
        return f"https://ordinalswallet.com/collection/{self.id}"

    @hybrid_property
    def num_inscriptions(self) -> int:
        return len(self.inscriptions)

    def inscriptions_iter(self) -> Iterator[InscriptionModel]:
        return iter(self.inscriptions)

    # TODO: methods like overall_size, time-frame of minting, etc.


if __name__ == "__main__":
    # Create the table in the database
    Base.metadata.create_all(get_engine())
