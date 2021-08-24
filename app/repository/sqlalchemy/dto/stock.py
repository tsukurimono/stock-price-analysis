from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (Column, String, Date, Integer, Float, Boolean, ForeignKey)

Base = declarative_base()

class DtoCandlestick(Base):
    __tablename__ = 'candlesticks'

    code         = Column('code', String(20), primary_key=True)
    market       = Column('market', String(20), primary_key=True)
    date         = Column('date', Date, primary_key=True)

    open_price   = Column('open', Float(asdecimal=True))
    close_price  = Column('close', Float(asdecimal=True))
    high_price   = Column('high', Float(asdecimal=True))
    low_price    = Column('low', Float(asdecimal=True))

    volume       = Column('volume', Integer)
    patched      = Column('patched', Boolean)

    def __repr__(self):
        return "<Candlestick(code='%s', market='%s', date='%s', open_price='%s', close_price='%s', high_price='%s', low_price='%s', volume='%s', patched='%s')>" % (self.code, self.market, self.date, self.open_price, self.high_price, self.low_price, self.volume, self.patched)

class DtoTag(Base):
    __tablename__ = 'tags'

    id   = Column('id', Integer, primary_key=True)
    name = Column('name', String(256))

    def __repr__(self):
        return "<DtoTag(id='%s', name='%s'>" % (self.id, self.name)

class DtoStockTag(Base):
    __tablename__ = 'stocks_tags'

    code    = Column('code', String(20), ForeignKey(DtoCandlestick.code,onupdate='CASCADE', ondelete='CASCADE'), primary_key=True)
    market  = Column('market', String(20), primary_key=True)
    tag_id  = Column('tag_id', Integer, primary_key=True)

    def __repr__(self):
        return "<DtoStockTag(code='%s', market='%s', tag_id='%s')>" % (self.code, self.market, self.tag_id)

class DtoDelisting(Base):
    __tablename__ = 'delistings'

    code         = Column('code', String(20), primary_key=True)
    market       = Column('market', String(20), primary_key=True)
    date         = Column('date', Date, primary_key=True)

    open_price   = Column('open', Float(asdecimal=True))
    close_price  = Column('close', Float(asdecimal=True))
    high_price   = Column('high', Float(asdecimal=True))
    low_price    = Column('low', Float(asdecimal=True))

    volume       = Column('volume', Integer)
    patched      = Column('patched', Boolean)

    def __repr__(self):
        return "<Delistings(code='%s', market='%s', date='%s', open_price='%s', close_price='%s', high_price='%s', low_price='%s', volume='%s', patched='%s')>" % (self.code, self.market, self.date, self.open_price, self.high_price, self.low_price, self.volume, self.patched)
