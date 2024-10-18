# models.py
from sqlalchemy import Column, BigInteger, String, Text, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

def create_models():
    class Channel(Base):
        __tablename__ = "transformed_channel"  

        channel_id = Column(BigInteger, primary_key=True, index=True)
        channel_username = Column(String, nullable=True)
        channel_title = Column(String, nullable=True)

        # Relationship to the TransformedProduct
        products = relationship("TransformedProduct", back_populates="channel")

    class TransformedProduct(Base):
        __tablename__ = 'transformed_product'

        product_id = Column(BigInteger, primary_key=True, nullable=False)  # Set as the primary key
        product_name = Column(Text, nullable=True)
        price_in_birr = Column(Integer, nullable=True)
        channel_id = Column(BigInteger, ForeignKey('transformed_channel.channel_id'))

        # Define back reference to TransformedChannel
        channel = relationship("Channel", back_populates="products")

    return Channel, TransformedProduct

# Usage example
Channel, TransformedProduct = create_models()