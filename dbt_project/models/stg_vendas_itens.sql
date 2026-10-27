-- Receita 1: junta itens de pedidos validos com o produto
{{ config(materialized='view') }}

select
    i.item_id,
    i.pedido_id,
    p.data_pedido,
    p.canal_venda,
    p.cliente_id,
    pr.categoria,
    i.quantidade,
    i.valor_liquido
from {{ source('silver', 'itens_pedido') }} i
join {{ source('silver', 'pedidos') }}  p  on p.pedido_id  = i.pedido_id
join {{ source('silver', 'produtos') }} pr on pr.produto_id = i.produto_id
where p.pedido_valido
