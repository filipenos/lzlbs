**Antes de iniciar você vai precisar de:**

[docker](https://www.docker.com)

[python3](https://www.python.org/downloads/)

**Para rodar o projecto siga as orientações:**

` git clone https://github.com/filipenos/lzlbs.git`

` cd lzlbs`

`make run-mysql` *aguarde 1 minuto enquanto o mysql é iniciado*

`make setup-mysql`

`make install-deps`

`make run`

A API ficará disponível  em: [http://localhost:5000](http://localhost:5000/)

A chave para autenticação da API é: **0123456789**

A documentação completa pode ser encontrada em: [http://localhost:5000/swagger](http://localhost:5000/swagger)
