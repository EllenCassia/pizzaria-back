from fastapi import FastAPI

def create_application() -> FastAPI:
    application = FastAPI(
        title="Pizzaria API",
        description="API para gerenciamento de uma pizzaria",
        contact={
            "name": "Ellen Cassia Rodrigues Matos Silva", 
            "email": "ellencassiamatos@gmail.com",
            "url": "https://seu-github.com",
        },
    )
    
    # Inclua os roteadores
    from pizzaria_api.presentation.controller.user_controller import router as user_router
    from pizzaria_api.presentation.controller.category_controller import router as category_router
    from pizzaria_api.presentation.controller.product_controller import router as product_router
    from pizzaria_api.presentation.controller.order_controller import router as order_router
    
    application.include_router(user_router, prefix="/users", tags=["users"])
    application.include_router(category_router, prefix="/categories", tags=["categories"])
    application.include_router(product_router, prefix="/products", tags=["products"])
    application.include_router(order_router, prefix="/orders", tags=["orders"])
    
    return application

app = create_application()
