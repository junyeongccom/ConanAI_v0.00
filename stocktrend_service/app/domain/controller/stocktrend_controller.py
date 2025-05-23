from ..service.stocktrend_service import StocktrendService

class StocktrendController:
    def __init__(self):
        self.service = StocktrendService()
    
    async def get_hello(self):
        return await self.service.get_hello()
