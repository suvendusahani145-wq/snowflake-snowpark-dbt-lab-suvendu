{{% config(materialized='Table',
            schema= 'Bronze',
        )%}}

select ID,
       TYPE,
       SYMBOL,
       PRICE,
       VOLUME,
       TRADE_TIMESTAMP,
       TRADE_CONDITIONS,
       case when TRADE_CONDITIONS=1 then "RRGULAR"
            when TRADE_CONDITIONS=8 then 'ODD_LOT'
            WHEN TRADE_CONDITIONS=24 then "EXTENDED_HOURS"
            END AS TRADE_CONDITION_GROUP
    from {{ref('Bronze_STOCK_TRADES')}}