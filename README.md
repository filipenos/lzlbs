**Antes de iniciar você vai precisar de:**

[https://www.docker.com](https://www.docker.com)

[https://www.python.org](https://www.python.org/downloads/)

[https://pip.pypa.io/en/stable/](https://pip.pypa.io/en/stable/)

**Para verificar se tudo está instalado**

    docker version
    python3 --version
    pip3 --version

**Você ira precisar da uma dependência do mysql libmysqlclient-dev**

*Instalação em ambientes ubuntu/debian*

    sudo apt install libmysqlclient-dev

*Instalação em ambientes mac*

    brew install libmysqlclient-dev

**Para rodar o projecto siga as orientações:**

    git clone https://github.com/filipenos/lzlbs.git

    cd lzlbs

    make run-mysql 

*aguarde 1 minuto enquanto o mysql é iniciado*

    make setup-mysql

    make run

A API ficará disponível  em: [http://localhost:5000](https://localhost:5000/)

A chave para autenticação da API é: **0123456789**

Para efetuar qualquer operação é necessário antes efetuar a autorização, para isso:
**POST** */api/auth*
**HEADER** *Content-Type: application/json* **required**

    {
      "key": "0123456789"
    }

O servidor retornará um token que deve ser enviado em todas as requisições como um header
Authorization: "Bearer token"

    {
      "Authorization":  "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJrZXkiOiIwMTIzNDU2Nzg5IiwiZXhwIjoxNTY4ODM5NzAzfQ.8gi2JBmC_FtIDZiEQwfIm0WgG-Df_5xLuYp53FwnP9E"
    }

Com isso é possível cadastrar um novo cliente, e suas lista de produtos favoritos.

A documentação completa pode ser encontrada em: [http://localhost:5000/swagger](http://localhost:5000/swagger)
