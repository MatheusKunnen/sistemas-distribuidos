# Sistema de monitamento do uso de CPU e RAM

A aplicação é um sistema de monitoramento do uso de cpu e ram, onde um módulo é encarregado de ler os parâmetros do sistema e atualizar os tópicos associados a estes parâmetros no broker (RabbitMQ). O sistema consite de dois módulos: o Publisher e o subscriber. O Publisher lê os parâmetros do sistema e os publica nos tópicos, no entanto, o subscriber se atualiza o gráfico cada vez que o tópico monitorado é atualizado.

## Requerimentos

- Python 3.10
- Biblioteca `pika` (Conexão com o broker)
- Biblioteca `psutil` (Leitura de parâmetros)
- Bibliotecas `numpy` e `matplotlib` (Gerar gráficos)
