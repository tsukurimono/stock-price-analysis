from app.repository.sqlalchemy.dto.stock import DtoCandlestick, DtoTag, DtoStockTag, DtoDelisting
from sqlalchemy import func, and_
from app.util.exception import InvalidDataAppException

from app.repository.stock import StockRepository
from app.repository.transaction import TxContext

from app.domain.stock import Candlestick, Interval

from app.repository.inputdata.stock  import *
from app.repository.outputdata.stock import *

class SqlalchemyStockRepository(StockRepository): 
    # ---------------------------------------------------------------------------------
    # Find candlestick dto.
    # ---------------------------------------------------------------------------------
    def find(self, ctx: TxContext, input_data:FindInput) -> FindOutput:
        code   = input_data.code
        market = input_data.market
        date   = input_data.date

        tx = ctx.get_tx()
        dto_candlestick = tx.query(DtoCandlestick).get((code, market, date))
        if dto_candlestick == None:
            return FindOutput(
                    candlestick = None
                    )

        result = Candlestick(
                code        = dto_candlestick.code,
                market      = dto_candlestick.market,
                date        = dto_candlestick.date,
                open_price  = dto_candlestick.open_price,
                close_price = dto_candlestick.close_price,
                high_price  = dto_candlestick.high_price,
                low_price   = dto_candlestick.low_price,
                volume      = dto_candlestick.volume,
                interval    = Interval.DAILY,
                patched     = dto_candlestick.patched
                )

        return FindOutput(
                candlestick = result
                )

    # ---------------------------------------------------------------------------------
    # Find tags.
    # ---------------------------------------------------------------------------------
    def find_tag(self, ctx: TxContext, input_data:FindTagInput) -> FindTagOutput:
        code   = input_data.code
        market = input_data.market

        tx = ctx.get_tx()
        dto_tags = tx.query(DtoTag).join(DtoStockTag, DtoStockTag.tag_id == DtoTag.id).filter(
                DtoStockTag.code == code,
                DtoStockTag.market == market
                )
        if dto_tags == None:
            return FindTagOutput(tags = [])

        result = []
        for dto_tag in dto_tags:
            result.append(dto_tag.name)

        return FindTagOutput(
                tags = result
                )

    # ---------------------------------------------------------------------------------
    # Create candlestick.
    # ---------------------------------------------------------------------------------
    def save(self, ctx: TxContext, input_data:SaveInput) -> SaveOutput:
        candlestick = input_data.candlestick

        tx = ctx.get_tx()
        dto_candlestick = tx.query(DtoCandlestick).get((candlestick.code, candlestick.market, candlestick.date))

        if dto_candlestick == None:
            tx.add(DtoCandlestick( 
                code        = candlestick.code, 
                market      = candlestick.market, 
                date        = candlestick.date, 
                open_price  = candlestick.open_price, 
                close_price = candlestick.close_price, 
                high_price  = candlestick.high_price, 
                low_price   = candlestick.low_price, 
                volume      = candlestick.volume,
                patched     = candlestick.patched
                ))
        else:
            dto_candlestick.open_price  = candlestick.open_price
            dto_candlestick.close_price = candlestick.close_price
            dto_candlestick.high_price  = candlestick.high_price
            dto_candlestick.low_price   = candlestick.low_price
            dto_candlestick.volume      = candlestick.volume

        return SaveOutput()

    # ---------------------------------------------------------------------------------
    # Create tags.
    # ---------------------------------------------------------------------------------
    def save_tag(self, ctx: TxContext, input_data:SaveTagInput) -> SaveTagOutput:
        stock = input_data.stock

        tag_ids = []
        tx = ctx.get_tx()
        for tag in stock.tags:
            got_tag = tx.query(DtoTag).filter(DtoTag.name == tag).first()
            if got_tag == None:
                dto = DtoTag(name = tag)
                tx.add(dto)
                tx.flush() # dto.id is determined here.
                tag_ids.append(dto.id)
            else:
                tag_ids.append(got_tag.id)

        _ = tx.query(DtoStockTag).filter(DtoStockTag.code == stock.code, DtoStockTag.market == stock.market).delete()
        for tag_id in tag_ids: 
            tx.add(DtoStockTag( 
                code   = stock.code, 
                market = stock.market, 
                tag_id = tag_id
                ))

        return SaveTagOutput()

    # ---------------------------------------------------------------------------------
    # Get candlesticks.
    # ---------------------------------------------------------------------------------
    def get(self, ctx: TxContext, input_data:GetInput) -> GetOutput:
        code      = input_data.code
        market    = input_data.market
        from_date = input_data.from_date
        to_date   = input_data.to_date

        tx = ctx.get_tx()
        dto_candlesticks = tx.query(DtoCandlestick).filter(
                DtoCandlestick.code   == code,
                DtoCandlestick.market == market,
                DtoCandlestick.date   >= from_date,
                DtoCandlestick.date   <= to_date
                ).order_by(DtoCandlestick.date.asc())

        result = [Candlestick(
                code        = dto.code,
                market      = dto.market,
                date        = dto.date,
                open_price  = dto.open_price,
                close_price = dto.close_price,
                high_price  = dto.high_price,
                low_price   = dto.low_price,
                volume      = dto.volume,
                patched     = dto.patched,
                interval    = Interval.DAILY
                ) for dto in dto_candlesticks]

        return GetOutput(
                candlesticks = result
                )

    # ---------------------------------------------------------------------------------
    # Get one's all candlesticks in target code.
    # ---------------------------------------------------------------------------------
    def get_ones_all(self, ctx: TxContext, input_data:GetOnesAllInput) -> GetOnesAllOutput:
        code      = input_data.code
        market    = input_data.market
        from_date = input_data.from_date
        to_date   = input_data.to_date

        filters = []
        filters.append(and_(DtoCandlestick.code == code))
        filters.append(and_(DtoCandlestick.market == market))

        if from_date != None: 
            filters.append(and_(DtoCandlestick.date >= from_date))

        if to_date != None: 
            filters.append(and_(DtoCandlestick.date <= to_date))

        tx = ctx.get_tx()
        dto_candlesticks = tx.query(DtoCandlestick).filter(
                *filters
                ).order_by(DtoCandlestick.code.asc(), DtoCandlestick.date.desc()).all()

        result = list()
        for dto in dto_candlesticks:
            result.append( 
                    Candlestick( 
                        code        = dto.code,
                        market      = dto.market,
                        date        = dto.date,
                        open_price  = dto.open_price,
                        close_price = dto.close_price,
                        high_price  = dto.high_price,
                        low_price   = dto.low_price,
                        volume      = dto.volume,
                        patched     = dto.patched,
                        interval    = Interval.DAILY
                        )
                    )
        return GetOnesAllOutput(
                candlesticks = result
                )

    # ---------------------------------------------------------------------------------
    # Get all candlesticks in target market.
    # ---------------------------------------------------------------------------------
    def get_all(self, ctx: TxContext, input_data:GetAllInput) -> GetAllOutput:
        market    = input_data.market
        tags      = input_data.tags
        from_date = input_data.from_date
        to_date   = input_data.to_date

        filters   = []
        filters.append(and_(
            DtoCandlestick.date   >= from_date, 
            DtoCandlestick.date   <= to_date
            ))

        tx = ctx.get_tx()
        query = tx.query(DtoCandlestick)
        if market != '':
            filters.append(and_(DtoCandlestick.market == market))

        if tags != []:
            filters.append(and_(DtoTag.name.in_(tags)))
            query = query.join(DtoStockTag, and_( 
                DtoStockTag.code == DtoCandlestick.code, 
                DtoStockTag.market == DtoCandlestick.market
                )).join(DtoTag, DtoStockTag.tag_id == DtoTag.id)

        dto_candlesticks = query.filter(
                    *filters
                ).order_by(DtoCandlestick.code.asc(), DtoCandlestick.date.desc())

        result = dict()
        for dto in dto_candlesticks:
            if dto.code not in result:
                result[dto.code] = list()
            result[dto.code].append(
                    Candlestick( 
                        code        = dto.code,
                        market      = dto.market,
                        date        = dto.date,
                        open_price  = dto.open_price,
                        close_price = dto.close_price,
                        high_price  = dto.high_price,
                        low_price   = dto.low_price,
                        volume      = dto.volume,
                        patched     = dto.patched,
                        interval    = Interval.DAILY
                        )
                    )
        return GetOutput(
                candlesticks = result
                )

    # ---------------------------------------------------------------------------------
    # Get each candlesticks in target market.
    # ---------------------------------------------------------------------------------
    def get_each(self, ctx: TxContext, input_data:GetEachInput) -> GetEachOutput:
        market    = input_data.market
        tags      = input_data.tags
        offset    = input_data.offset 
        today     = input_data.today

        filters   = []

        if market != '': 
            filters.append(and_(DtoCandlestick.market == market))

        tx = ctx.get_tx()
        query = tx.query(DtoCandlestick.code, DtoCandlestick.market)

        if tags != []:
            filters.append(and_(DtoTag.name.in_(tags)))
            query = query.join(DtoStockTag, and_( 
                DtoStockTag.code == DtoCandlestick.code, 
                DtoStockTag.market == DtoCandlestick.market
                )).join(DtoTag, DtoStockTag.tag_id == DtoTag.id)

        dto_codes = query.filter(
                *filters
                ).group_by(DtoCandlestick.code, DtoCandlestick.market).all()

        result = dict()
        for dto_code in dto_codes:
            dto_candlestick = tx.query(DtoCandlestick).filter(
                    DtoCandlestick.code   == dto_code[0],
                    DtoCandlestick.market == dto_code[1],
                    DtoCandlestick.date   <= today, 
                    ).order_by(DtoCandlestick.date.desc()).offset(offset).limit(1).first()
            if dto_candlestick == None:
                continue

            result[dto_candlestick.code] = Candlestick( 
                    code        = dto_candlestick.code,
                    market      = dto_candlestick.market,
                    date        = dto_candlestick.date,
                    open_price  = dto_candlestick.open_price,
                    close_price = dto_candlestick.close_price,
                    high_price  = dto_candlestick.high_price,
                    low_price   = dto_candlestick.low_price,
                    volume      = dto_candlestick.volume,
                    patched     = dto_candlestick.patched,
                    interval    = Interval.DAILY
                    )

        return GetEachOutput(
                candlesticks = result
                )

    # ---------------------------------------------------------------------------------
    # Get range candlesticks in target market.
    # ---------------------------------------------------------------------------------
    def get_range(self, ctx: TxContext, input_data:GetRangeInput) -> GetRangeOutput:
        code    = input_data.code
        market  = input_data.market
        tags    = input_data.tags
        to_date = input_data.to_date 
        limit   = input_data.limit 

        filters   = []

        if code != '': 
            filters.append(and_(DtoCandlestick.code == code))

        if market != '': 
            filters.append(and_(DtoCandlestick.market == market))

        tx = ctx.get_tx()
        query = tx.query(DtoCandlestick.code, DtoCandlestick.market)

        if tags != []:
            filters.append(and_(DtoTag.name.in_(tags)))
            query = query.join(DtoStockTag, and_( 
                DtoStockTag.code == DtoCandlestick.code, 
                DtoStockTag.market == DtoCandlestick.market
                )).join(DtoTag, DtoStockTag.tag_id == DtoTag.id)

        dto_codes = query.filter(
                *filters
                ).group_by(DtoCandlestick.code, DtoCandlestick.market).all()

        result = dict()
        for dto_code in dto_codes:
            dto_candlesticks = tx.query(DtoCandlestick).filter(
                    DtoCandlestick.code   == dto_code[0],
                    DtoCandlestick.market == dto_code[1],
                    DtoCandlestick.date   <= to_date
                    ).order_by(DtoCandlestick.date.desc()).limit(limit).all()
            if len(dto_candlesticks) == 0:
                continue

            result[dto_code[0]] = [Candlestick( 
                    code        = dto.code,
                    market      = dto.market,
                    date        = dto.date,
                    open_price  = dto.open_price,
                    close_price = dto.close_price,
                    high_price  = dto.high_price,
                    low_price   = dto.low_price,
                    volume      = dto.volume,
                    patched     = dto.patched,
                    interval    = Interval.DAILY
                    ) for dto in dto_candlesticks]

        return GetRangeOutput(
                candlesticks = result
                )

    # ---------------------------------------------------------------------------------
    # Search tickers.
    # ---------------------------------------------------------------------------------
    def search_tickers(self, ctx: TxContext, input_data:SearchTickersInput) -> SearchTickersOutput:
        keyword = input_data.keyword

        tx = ctx.get_tx()
        dto_candlesticks = tx.query(DtoCandlestick.code, DtoCandlestick.market).filter(
                DtoCandlestick.code.like(f"%{keyword}%")
                ).group_by(DtoCandlestick.code, DtoCandlestick.market)

        result = [SearchTickersOutput.Ticker(
            code   = dto.code,
            market = dto.market
            ) for dto in dto_candlesticks]

        return SearchTickersOutput(
                tickers = result
                )

    # ---------------------------------------------------------------------------------
    # Search markets.
    # ---------------------------------------------------------------------------------
    def search_markets(self, ctx: TxContext, input_data:SearchMarketsInput) -> SearchMarketsOutput:
        keyword = input_data.keyword

        tx = ctx.get_tx()
        dto_candlesticks = tx.query(DtoCandlestick.market).filter(
                DtoCandlestick.market.like(f"%{keyword}%")
                ).group_by(DtoCandlestick.market)

        result = [dto.market for dto in dto_candlesticks]

        return SearchMarketsOutput(
                markets = result
                )

    # ---------------------------------------------------------------------------------
    # Search tags.
    # ---------------------------------------------------------------------------------
    def search_tags(self, ctx: TxContext, input_data:SearchTagsInput) -> SearchTagsOutput:
        keyword = input_data.keyword

        tx = ctx.get_tx()
        dto_tags = tx.query(DtoTag.name).filter(
                DtoTag.name.like(f"%{keyword}%")
                ).group_by(DtoTag.name)

        result = [dto.name for dto in dto_tags]

        return SearchTagsOutput(
                tags = result
                )

    # ---------------------------------------------------------------------------------
    # Get stock data info.
    # ---------------------------------------------------------------------------------
    def get_stockdatainfo(self, ctx: TxContext, input_data:GetStockdatainfoInput) -> GetStockdatainfoOutput:
        code   = input_data.code
        market = input_data.market

        tx = ctx.get_tx()
        dto_info = tx.query(func.min(DtoCandlestick.date), func.max(DtoCandlestick.date), func.max(DtoCandlestick.close_price), func.min(DtoCandlestick.close_price), func.max(DtoCandlestick.high_price), func.min(DtoCandlestick.low_price)).filter(
                DtoCandlestick.market == market,
                DtoCandlestick.code   == code,
                ).group_by(
                DtoCandlestick.market,
                DtoCandlestick.code
                ).first()

        return GetStockdatainfoOutput(
                first_date      = dto_info[0],
                last_date       = dto_info[1],
                close_price_ath = dto_info[2],
                close_price_atl = dto_info[3],
                high_price_ath  = dto_info[4],
                low_price_atl   = dto_info[5],
                )

    # ---------------------------------------------------------------------------------
    # Get stock data info.
    # ---------------------------------------------------------------------------------
    def get_tickers(self, ctx: TxContext, input_data:GetTickersInput) -> GetTickersOutput:
        market = input_data.market

        tx = ctx.get_tx()
        dto_candlesticks = tx.query(DtoCandlestick.code, DtoCandlestick.market).filter(
                DtoCandlestick.market == market,
                ).group_by(
                DtoCandlestick.code
                ).all()

        return GetTickersOutput(
                tickers = [GetTickersOutput.Ticker(
                    code   = dto.code,
                    market = dto.market
                    ) for dto in dto_candlesticks]
                )

    # ---------------------------------------------------------------------------------
    # Create delisting.
    # ---------------------------------------------------------------------------------
    def save_delisting(self, ctx: TxContext, input_data:SaveDelistingInput) -> SaveDelistingOutput:
        delisting = input_data.delisting

        tx = ctx.get_tx()
        dto_delisting = tx.query(DtoDelisting).get((delisting.code, delisting.market, delisting.date))

        if dto_delisting == None:
            tx.add(DtoDelisting( 
                code        = delisting.code, 
                market      = delisting.market, 
                date        = delisting.date, 
                open_price  = delisting.open_price, 
                close_price = delisting.close_price, 
                high_price  = delisting.high_price, 
                low_price   = delisting.low_price, 
                volume      = delisting.volume,
                patched     = delisting.patched
                ))
        else:
            dto_delisting.open_price  = delisting.open_price
            dto_delisting.close_price = delisting.close_price
            dto_delisting.high_price  = delisting.high_price
            dto_delisting.low_price   = delisting.low_price
            dto_delisting.volume      = delisting.volume

        return SaveDelistingOutput()

    # ---------------------------------------------------------------------------------
    # Find delisting dto.
    # ---------------------------------------------------------------------------------
    def find_delisting(self, ctx: TxContext, input_data:FindDelistingInput) -> FindDelistingOutput:
        code   = input_data.code
        market = input_data.market
        date   = input_data.date

        tx = ctx.get_tx()
        dto_delisting = tx.query(DtoDelisting).get((code, market, date))
        if dto_delisting == None:
            return FindDelistingOutput(
                    delisting = None
                    )

        result = Candlestick(
                code        = dto_delisting.code,
                market      = dto_delisting.market,
                date        = dto_delisting.date,
                open_price  = dto_delisting.open_price,
                close_price = dto_delisting.close_price,
                high_price  = dto_delisting.high_price,
                low_price   = dto_delisting.low_price,
                volume      = dto_delisting.volume,
                interval    = Interval.DAILY,
                patched     = dto_delisting.patched
                )

        return FindDelistingOutput(
                delisting = result
                )

    # ---------------------------------------------------------------------------------
    # Remove target all sticks.
    # ---------------------------------------------------------------------------------
    def remove_ones_all(self, ctx: TxContext, input_data:RemoveOnesAllInput) -> RemoveOnesAllOutput:
        code   = input_data.code
        market = input_data.market

        tx = ctx.get_tx()
        _ = tx.query(DtoStockTag).filter(DtoStockTag.code == code, DtoStockTag.market == market).delete()
        _ = tx.query(DtoCandlestick).filter(DtoCandlestick.code == code, DtoCandlestick.market == market).delete()

        return RemoveOnesAllOutput()

    # ---------------------------------------------------------------------------------
    # Get one's all delistings in target code.
    # ---------------------------------------------------------------------------------
    def get_delistings_ones_all(self, ctx: TxContext, input_data:GetDelistingsOnesAllInput) -> GetDelistingsOnesAllOutput:
        code      = input_data.code
        market    = input_data.market
        from_date = input_data.from_date
        to_date   = input_data.to_date

        filters = []
        filters.append(and_(DtoDelisting.code == code))
        filters.append(and_(DtoDelisting.market == market))

        if from_date != None: 
            filters.append(and_(DtoDelisting.date >= from_date))

        if to_date != None: 
            filters.append(and_(DtoDelisting.date <= to_date))

        tx = ctx.get_tx()
        dto_delistings = tx.query(DtoDelisting).filter(
                *filters
                ).order_by(DtoDelisting.code.asc(), DtoDelisting.date.desc()).all()

        result = list()
        for dto in dto_delistings:
            result.append( 
                    Candlestick( 
                        code        = dto.code,
                        market      = dto.market,
                        date        = dto.date,
                        open_price  = dto.open_price,
                        close_price = dto.close_price,
                        high_price  = dto.high_price,
                        low_price   = dto.low_price,
                        volume      = dto.volume,
                        patched     = dto.patched,
                        interval    = Interval.DAILY
                        )
                    )
        return GetDelistingsOnesAllOutput(
                delistings = result
                )

    # ---------------------------------------------------------------------------------
    # Remove target all delistings.
    # ---------------------------------------------------------------------------------
    def remove_delistings_ones_all(self, ctx: TxContext, input_data:RemoveDelistingsOnesAllInput) -> RemoveDelistingsOnesAllOutput:
        code   = input_data.code
        market = input_data.market

        tx = ctx.get_tx()
        _ = tx.query(DtoDelisting).filter(DtoDelisting.code == code, DtoDelisting.market == market).delete()

        return RemoveDelistingsOnesAllOutput()

    # ---------------------------------------------------------------------------------
    # Get all term information of candlesticks.
    # ---------------------------------------------------------------------------------
    def get_all_term(self, ctx: TxContext, input_data:GetAllTermInput) -> GetAllTermOutput:
        tx = ctx.get_tx()
        dto_candlesticks = tx.query(
                DtoCandlestick.code,
                DtoCandlestick.market,
                func.max(DtoCandlestick.date).label("last_date"),
                func.min(DtoCandlestick.date).label("first_date"),
                ).group_by(DtoCandlestick.code, DtoCandlestick.market).all()

        result = list()
        for dto in dto_candlesticks:
            result.append( 
                    Term( 
                        code       = dto[0],
                        market     = dto[1],
                        last_date  = dto[2],
                        first_date = dto[3]
                        )
                    )
        return GetAllTermOutput(
                terms = result
                )

    # ---------------------------------------------------------------------------------
    # Remove tag.
    # ---------------------------------------------------------------------------------
    def remove_tag(self, ctx: TxContext, input_data:RemoveTagInput) -> RemoveTagOutput:
        tagname = input_data.tagname

        tx = ctx.get_tx()
        tag = tx.query(DtoTag).filter(DtoTag.name == tagname).first()
        if tag != None: 
            _ = tx.query(DtoStockTag).filter(DtoStockTag.tag_id == tag.id).delete()

        return RemoveTagOutput()
