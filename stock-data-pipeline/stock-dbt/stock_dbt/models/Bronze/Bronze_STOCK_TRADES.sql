{{% config(materialized='Table',
            schema= 'Bronze',
        )%}}

select ID,
       TYPE,
       SYMBOL,
       PRICE,
       VOLUME,
       converttimezone('UTC',TRADE_TIMESTAMP),
       f.value::STRING as TRADE_CONDITIONS
    from {{source(raw,'STOCK_TRADES')}} t,
         LATERL FLATTEN(INPUT => t.TRADE_CONDITIONS) f
