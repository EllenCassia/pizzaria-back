import uuid
from sqlalchemy import UUID, Column, Float, ForeignKey, String, Integer, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship
from pizzaria_api.contrib.models import BaseModel

class User(BaseModel):
    __tablename__ = 'users'

    pk_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name_empresa: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(50), nullable=False)
    password: Mapped[str] = mapped_column(String(225), nullable=False)

    def __repr__(self):
        # Retorna uma representação do objeto
        return f'User(pk_id={self.pk_id}, name_empresa={self.name_empresa}, email={self.email})'
    
class Category(BaseModel):
    __tablename__ = "categories"
    
    pk_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    products: Mapped[list["Product"]] = relationship("Product", back_populates="category")

    def __repr__(self):
        # Retorna uma representação do objeto
        return f'Category(pk_id={self.pk_id}, name={self.name}, products={self.products})'


order_product_association = Table(
    "order_product_association", BaseModel.metadata,
    Column("order_id", Integer, ForeignKey("orders.pk_id"), primary_key=True),
    Column("product_id", Integer, ForeignKey("products.pk_id"), primary_key=True)
)
class Product(BaseModel):
    __tablename__ = "products"
     
    pk_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, unique=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    describe: Mapped[str] = mapped_column(String(100), nullable=False)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.pk_id"))
    category: Mapped["Category"] = relationship("Category", back_populates="products")

    # Relacionamento recíproco com Order
    orders: Mapped[list["Order"]] = relationship(
        "Order",
        secondary=order_product_association,  # Tabela de associação
        back_populates="products"  # Relacionamento recíproco no modelo Order
    )

    def __repr__(self):
        return f'Product(pk_id={self.pk_id}, name={self.name}, price={self.price}, category_id={self.category_id})' 

class Order(BaseModel):
    __tablename__ = "orders"

    pk_id: Mapped[int] = mapped_column(Integer, primary_key=True,autoincrement=True,unique=True)
    amount: Mapped[int] = mapped_column(Integer, nullable=False)
    number_table: Mapped[int] = mapped_column(Integer, nullable=False)

    # Relacionamento com Product via tabela de associação
    products: Mapped[list["Product"]] = relationship(
        "Product",
        secondary=order_product_association,  # Tabela de associação
        back_populates="orders"  # Relacionamento recíproco no modelo Product
    )

    def __repr__(self):
        return (f'Order(pk_id={self.pk_id}, amount={self.amount},'
                f'products={self.products}, number_table={self.number_table})')
    