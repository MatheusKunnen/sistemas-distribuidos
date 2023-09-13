# Sistema de monitamento do uso de CPU e RAM

A aplicação é um sistema de monitoramento do uso de CPU e RAM, onde um módulo é encarregado de ler os parâmetros do sistema e atualizar os tópicos associados a estes parâmetros no broker (RabbitMQ). O sistema consiste de dois módulos: o Publisher e o Subscriber. O Publisher lê os parâmetros do sistema e os publica nos tópicos, enquanto o Subscriber mantém-se atualizado com as informações provenientes dos tópicos monitorados e, sempre que esses tópicos são atualizados, ele atualiza os gráficos correspondentes.

## Requerimentos

- Python 3.10
- Biblioteca `pika` (Conexão com o broker)
- Biblioteca `psutil` (Leitura de parâmetros)
- Bibliotecas `numpy` e `matplotlib` (Gerar gráficos)
