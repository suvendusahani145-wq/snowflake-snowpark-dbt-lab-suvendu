{{% config(materialized= 'Table'
           schema= 'Bronze'%}}

select CURRENCY,
       DESCRIPTION,
       DISPLAYSYMBOL,
       FIGI,
       FIGICOMPOSITE.
       ISIN,
       MIC,
       SHARECLASSFIGI,
       SYMBOL,
       SYMBOL2,
       TYPE
       from {{source('raw','DIM_SYMBOLS')}}