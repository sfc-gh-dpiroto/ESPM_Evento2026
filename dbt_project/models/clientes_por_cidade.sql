-- Receita 3: onde estao os clientes que compram
select
    c.cidade,
    c.uf,
    count(distinct v.cliente_id)        as clientes,
    count(distinct v.pedido_id)         as pedidos,
    sum(v.valor_liquido)::number(14,2)  as receita
from {{ ref('stg_vendas_itens') }} v
join {{ source('silver', 'clientes') }} c on c.cliente_id = v.cliente_id
group by c.cidade, c.uf
