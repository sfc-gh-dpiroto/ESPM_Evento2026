-- Receita 2: quanto cada categoria vende (usa a receita 1 via ref)
select
    categoria,
    count(distinct pedido_id)          as pedidos,
    sum(quantidade)                    as unidades,
    sum(valor_liquido)::number(14,2)   as receita
from {{ ref('stg_vendas_itens') }}
group by categoria
