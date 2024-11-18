select 
    `Adj Close`,
    Date
from historico
where ticker = {{ticker|string}}
AND Date BETWEEN {{start|string}} AND {{end|string}}
;