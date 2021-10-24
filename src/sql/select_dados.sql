select *
from historico
where ticker = {{ticker}}
AND Date BETWEEN {{start}} AND {{end}}
;