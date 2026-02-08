import uuid

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.product import Category, Product

# Fixed UUIDs for seeding
CAT_API_ID = uuid.UUID("a1e1b1c1-d1e1-41f1-a1b1-c1d1e1f1a1b1")
CAT_DATA_ID = uuid.UUID("a2e2b2c2-d2e2-42f2-a2b2-c2d2e2f2a2b2")

PROD_WEATHER_API_ID = uuid.UUID("b1e1b1c1-d1e1-41f1-a1b1-c1d1e1f1a1b1")
PROD_FINANCE_API_ID = uuid.UUID("b2e2b2c2-d2e2-42f2-a2b2-c2d2e2f2a2b2")
PROD_GEO_DATA_ID = uuid.UUID("b3e3b3c3-d3e3-43f3-a3b3-c3d3e3f3a3b3")


async def init_db(db: AsyncSession) -> None:
    # Check if we already have categories
    result = await db.execute(select(Category).limit(1))
    category = result.scalar_one_or_none()

    if not category:
        # Create categories
        apis = Category(
            id=CAT_API_ID, name="API Services", description="Premium API endpoints"
        )
        data = Category(
            id=CAT_DATA_ID, name="Data Packages", description="Large scale datasets"
        )
        db.add_all([apis, data])

        # Create products
        weather_api = Product(
            id=PROD_WEATHER_API_ID,
            name="Weather API - Pro",
            description="Real-time global weather data with 5-day forecast.",
            price=49.99,
            stock=999999,
            category_id=CAT_API_ID,
            api_url="https://api.weather.example.com/v1",
            quota_limit=100000,
            rate_limit=1000,
        )
        finance_api = Product(
            id=PROD_FINANCE_API_ID,
            name="Finance API - Standard",
            description="Stock market data and currency exchange rates.",
            price=29.99,
            stock=999999,
            category_id=CAT_API_ID,
            api_url="https://api.finance.example.com/v1",
            quota_limit=50000,
            rate_limit=500,
        )
        geo_data = Product(
            id=PROD_GEO_DATA_ID,
            name="GeoJSON Data Pack",
            description="Detailed GeoJSON data for all world countries.",
            price=19.99,
            stock=999999,
            category_id=CAT_DATA_ID,
            api_url=None,
            quota_limit=0,
            rate_limit=0,
        )
        db.add_all([weather_api, finance_api, geo_data])

        await db.commit()
