{{% config(materialized='incremental',
            schema= 'Bronze',
            unique_key= TRADE_TIMESTAMP_UTC,
            incremtal_startegy= 'merge'
        )%}}

select ID,
       TYPE,
       SYMBOL,
       PRICE,
       VOLUME,
       converttimezone('UTC',TRADE_TIMESTAMP) as TRADE_TIMESTAMP_UTC,
       f.value::STRING as TRADE_CONDITIONS
    from {{source(raw,'STOCK_TRADES')}} t,
         LATERL FLATTEN(INPUT => t.TRADE_CONDITIONS) f

{{% if is_incremental()%}}
 where TRADE_TIMESTAMP_UTC >(select TRADE_TIMESTAMP_UTC from {{this}})
{{%end if%}}