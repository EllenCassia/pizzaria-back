from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from pizzaria_api.model.entity.models import Order

class OrderRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_order(self, order: Order) -> Order:
        try:
            async with self.session.begin():
                self.session.add(order)  
                await self.session.flush()  
                await self.session.commit()
                return order
        except Exception as e:
            await self.session.rollback()
            raise Exception(f"Error adding order: {e}")
        finally:
            await self.session.close()

    async def get_all_orders(self) -> List[Order]:
        try:
            stmt = select(Order)
            result = await self.session.execute(stmt)
            orders = result.scalars().all()
            return orders
        except Exception as e:
            raise Exception(f"Error getting orders: {e}")

    