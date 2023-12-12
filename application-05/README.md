# Aplicação-5

Esta aplicação implementa os processos realizados na compra de um snacks em uma vending machine. Onde a atualização de stock, registro da venda e registro do pagamento devem ser todos completados com sucesso ou anulados. O controle de stock é implementado pelo `StockParticipant`, o registro das vendas é gerenciado pelo `OrderParticipant` e finalmente o pagamento é realizado pelo `PaymentParticipant`.

## Classes principais

### Coordinator

Contém todas as operações de controle das transações. Os participantes se comunicam com o coordenador utilizando os endpoints REST definidos no arquivo `coordinator_i.py`

### Participant

Participante genêrico que gerencia a consistência dos dados e implementa as funções que formam parte da transação. Esta classe é utilizada pelos participantes `StockParticipant`, `PaymentParticipant` e `OrderParticipant`. O coordenador chama os seus métodos por meio de endpoints REST definidos nos arquivos `stock_i.py`, `payment_i.py` e `order_i.py`.

## Instruções de execução

- Iniciar o coordenador

```
python3 coordinator_i.py
```

- Iniciar participantes

```
python3 stock_i.py
python3 payment_i.py
python3 order_i.py
```

- Executar cliente

```
python3 client.py
```
