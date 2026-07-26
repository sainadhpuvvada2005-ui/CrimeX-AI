from sqlalchemy import Select, func, select
from sqlalchemy.orm import Session

from app.utils.pagination import PageParams


def paginate_query(db: Session, query: Select, params: PageParams):
    count_query = select(func.count()).select_from(query.order_by(None).subquery())
    total = db.execute(count_query).scalar_one()
    rows = db.execute(query.offset(params.offset).limit(params.size)).mappings().all()
    return rows, total

