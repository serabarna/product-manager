from contextlib import asynccontextmanager
from typing import List
from uuid import uuid4

from fastapi import Depends, FastAPI, HTTPException, Cookie, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from typing import Optional

from config import settings
from database import Product, Cart, CartItem, create_tables, get_db

class ProductDTO(BaseModel):
    id: int
    name: str
    price: float
    description: str | None = None
    stock: int

class ProductCreateDTO(BaseModel):
    name: str
    price: float
    description: str | None = None
    stock: int

class ProductUpdateDTO(BaseModel):
    name: str | None = None
    price: float | None = None
    description: str | None = None
    stock: int | None = None

class CartItemDTO(BaseModel):
    id: int
    product_id: int
    quantity: int
    product: ProductDTO

class CartDTO(BaseModel):
    id: int
    session_id: str
    items: List[CartItemDTO]

class AddToCartDTO(BaseModel):
    product_id: int
    quantity: int = 1

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    yield


from fastapi.responses import JSONResponse

app = FastAPI(title=settings.app_name, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin"],
    expose_headers=["Content-Type", "Set-Cookie"],
)

@app.get("/")
async def root():
    return {"message": "Welcome to FastAPI Template"}

@app.post("/products/", response_model=ProductDTO)
async def create_product(product: ProductCreateDTO, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Product).filter(Product.name == product.name))
    existing_product = result.scalar_one_or_none()
    if existing_product:
        raise HTTPException(status_code=400, detail="Product with this name already exists")
    db_product = Product(
        name=product.name,
        price=product.price,
        description=product.description,
        stock=product.stock
    )
    db.add(db_product)
    await db.commit()
    await db.refresh(db_product)
    return db_product

@app.get("/products/", response_model=List[ProductDTO])
async def get_products(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Product))
    products = result.scalars().all()
    return products

@app.get("/products/{product_id}", response_model=ProductDTO)
async def get_product(product_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Product).filter(Product.id == product_id))
    product = result.scalar_one_or_none()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.put("/products/{product_id}", response_model=ProductDTO)
async def update_product(product_id: int, product_update: ProductUpdateDTO, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Product).filter(Product.id == product_id))
    db_product = result.scalar_one_or_none()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    for field, value in product_update.model_dump(exclude_unset=True).items():
        setattr(db_product, field, value)
    db.add(db_product)
    await db.commit()
    await db.refresh(db_product)
    return db_product

@app.delete("/products/{product_id}", response_model=dict)
async def delete_product(product_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Product).filter(Product.id == product_id))
    db_product = result.scalar_one_or_none()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    await db.delete(db_product)
    await db.commit()
    return {"message": "Product deleted successfully"}

async def get_or_create_cart(
    response: Response,
    session_id: Optional[str] = Cookie(None),
    db: AsyncSession = Depends(get_db)
) -> Cart:
    if not session_id:
        session_id = str(uuid4())
        response.set_cookie(
            key="session_id",
            value=session_id,
            httponly=True,
            samesite="lax",
            max_age=7 * 24 * 60 * 60  # 1 week
        )

    result = await db.execute(
        select(Cart)
        .options(selectinload(Cart.items).selectinload(CartItem.product))
        .filter(Cart.session_id == session_id)
    )
    cart = result.scalar_one_or_none()

    if not cart:
        cart = Cart(session_id=session_id)
        db.add(cart)
        await db.commit()
        await db.refresh(cart)

    return cart, session_id

# Cart endpoints
@app.post("/cart/add", response_model=CartDTO)
async def add_to_cart(
    response: Response,
    item: AddToCartDTO,
    db: AsyncSession = Depends(get_db),
    cart_data: tuple[Cart, str] = Depends(get_or_create_cart)
):
    cart, session_id = cart_data
    
    # Get cart ID directly
    cart_id = cart.id
    
    # Check if product exists and has stock
    result = await db.execute(select(Product).filter(Product.id == item.product_id))
    product = result.scalar_one_or_none()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    if product.stock <= 0:
        raise HTTPException(status_code=400, detail="Product is out of stock")

    # Check if item already in cart
    result = await db.execute(
        select(CartItem).filter(
            CartItem.cart_id == cart_id,
            CartItem.product_id == item.product_id
        )
    )
    cart_item = result.scalar_one_or_none()

    if cart_item:
        # Update quantity if item exists
        cart_item.quantity = cart_item.quantity + item.quantity
    else:
        # Create new cart item
        cart_item = CartItem(
            cart_id=cart_id,
            product_id=item.product_id,
            quantity=item.quantity
        )
        db.add(cart_item)

    # Update product stock
    product.stock -= item.quantity
    await db.commit()
    
    # Load updated cart with items and products
    result = await db.execute(
        select(Cart)
        .options(selectinload(Cart.items).selectinload(CartItem.product))
        .filter(Cart.id == cart_id)
    )
    updated_cart = result.scalar_one()

    # Return response with loaded relationships
    return CartDTO(
        id=updated_cart.id,
        session_id=session_id,
        items=[
            CartItemDTO(
                id=cart_item.id,
                product_id=cart_item.product_id,
                quantity=cart_item.quantity,
                product=ProductDTO(
                    id=cart_item.product.id,
                    name=cart_item.product.name,
                    price=cart_item.product.price,
                    description=cart_item.product.description,
                    stock=cart_item.product.stock
                )
            )
            for cart_item in updated_cart.items
        ]
    )

@app.get("/cart", response_model=CartDTO)
async def get_cart(
    db: AsyncSession = Depends(get_db),
    cart_data: tuple[Cart, str] = Depends(get_or_create_cart)
):
    cart, session_id = cart_data
    cart_id = cart.id
    
    # Load cart with its items and products
    result = await db.execute(
        select(Cart)
        .options(selectinload(Cart.items).selectinload(CartItem.product))
        .filter(Cart.id == cart_id)
    )
    loaded_cart = result.scalar_one()

    return CartDTO(
        id=loaded_cart.id,
        session_id=session_id,
        items=[
            CartItemDTO(
                id=item.id,
                product_id=item.product_id,
                quantity=item.quantity,
                product=ProductDTO(
                    id=item.product.id,
                    name=item.product.name,
                    price=item.product.price,
                    description=item.product.description,
                    stock=item.product.stock
                )
            )
            for item in loaded_cart.items
        ]
    )

@app.delete("/cart/remove/{item_id}", response_model=CartDTO)
async def remove_from_cart(
    item_id: int,
    db: AsyncSession = Depends(get_db),
    cart_data: tuple[Cart, str] = Depends(get_or_create_cart)
):
    cart, session_id = cart_data
    
    # Find cart item
    result = await db.execute(select(CartItem).filter(CartItem.id == item_id))
    cart_item = result.scalar_one_or_none()
    
    if not cart_item or cart_item.cart_id != cart.id:
        raise HTTPException(status_code=404, detail="Cart item not found")

    # Return quantity to product stock
    result = await db.execute(select(Product).filter(Product.id == cart_item.product_id))
    product = result.scalar_one_or_none()
    if product:
        product.stock += cart_item.quantity
        db.add(product)

    # Remove item from cart
    await db.delete(cart_item)
    await db.commit()

    # Load updated cart with its items and products
    result = await db.execute(
        select(Cart)
        .options(selectinload(Cart.items).selectinload(CartItem.product))
        .filter(Cart.id == cart.id)
    )
    cart = result.scalar_one()

    return CartDTO(
        id=cart.id,
        session_id=session_id,
        items=[
            CartItemDTO(
                id=item.id,
                product_id=item.product_id,
                quantity=item.quantity,
                product=ProductDTO(
                    id=item.product.id,
                    name=item.product.name,
                    price=item.product.price,
                    description=item.product.description,
                    stock=item.product.stock
                )
            )
            for item in cart.items
        ]
    )

@app.delete("/products/{product_id}", response_model=dict)
async def delete_product(product_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Product).filter(Product.id == product_id))
    db_product = result.scalar_one_or_none()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    await db.delete(db_product)
    await db.commit()
    return {"detail": "Product deleted"}

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
