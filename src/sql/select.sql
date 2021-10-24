select count(*)
from historico
;

SELECT count(distinct ticker)
from historico
;

SELECT  ticker,
        count(*)
FROM historico

group by ticker
;