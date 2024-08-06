from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model import Base

engine = create_engine('postgresql://postgres:difyai123456@127.0.0.1:5432/test')

Base.metadata.create_all(engine)

# Session = sessionmaker(bind=engine)
# session = Session()
#
# # quote = Qutes(quote="I love", author="<NAME>", tags="[]")
# # session.add(quote)
# # session.commit()
#
# quotes = session.query(model.Qutes).all()
# urls = session.query(model.CnnyUrls).all()
# print(quotes.count)


# pythong db.py 创建数据表。已存在的表，不会重复创建