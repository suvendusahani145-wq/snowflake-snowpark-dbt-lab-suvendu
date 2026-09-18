{{% config(materialized='incremental',
            schema= 'Bronze',
            unique_key= TRADE_TIMESTAMP_UTC,
            incremtal_startegy= 'merge'
        )%}}

select ID,
       TYPE,
       SYMBOL,
       cast(PRICE as NUMBER(15,4))as PRICE,
       VOLUME,
       PRICE * VOLUME AS TRADE_VALUE,
       TRADE_TIMESTAMP,
       TRADE_CONDITIONS,
       case when TRADE_CONDITIONS=1 then "RRGULAR"
            when TRADE_CONDITIONS=8 then 'ODD_LOT'
            WHEN TRADE_CONDITIONS=24 then "EXTENDED_HOURS"
            END AS TRADE_CONDITION_GROUP
    from {{ref('Bronze_STOCK_TRADES')}}

{{if is_incremental()%}}
where TRADE_TIMESTAMP > (select TRADE_TIMESTAMP from {{this}})

