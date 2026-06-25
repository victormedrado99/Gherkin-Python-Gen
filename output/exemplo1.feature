```gherkin
# language: pt

Funcionalidade: Autenticação de Usuários

  Como um usuário do sistema
  Eu quero fazer login
  Para acessar minhas funcionalidades

  Cenário: Autenticação bem-sucedida com credenciais válidas
    Dado que existe um usuário com email "usuario_valido@exemplo.com" e senha "SenhaCorreta123" cadastrados
    Quando eu tento fazer login com email "usuario_valido@exemplo.com" e senha "SenhaCorreta123"
    Então eu devo ser redirecionado para o "dashboard"

  Cenário: Tentativa de login com email não cadastrado
    Dado que não existe um usuário com email "nao_cadastrado@exemplo.com"
    Quando eu tento fazer login com email "nao_cadastrado@exemplo.com" e senha "QualquerSenhaInvalida"
    Então o sistema deve exibir a mensagem "Usuário não encontrado"

  Cenário: Tentativa de login com senha incorreta para email cadastrado
    Dado que existe um usuário com email "usuario_existente@exemplo.com" e senha "SenhaCorreta456" cadastrados
    Quando eu tento fazer login com email "usuario_existente@exemplo.com" e senha "SenhaIncorreta789"
    Então o sistema deve exibir a mensagem "Senha inválida"

  Cenário: Bloqueio de conta após 3 tentativas falhas consecutivas e posterior tentativa de login
    Dado que existe um usuário com email "usuario_bloqueio@exemplo.com" e senha "SenhaSecreta789" cadastrados
    E que a conta "usuario_bloqueio@exemplo.com" não está bloqueada
    Quando eu realizo 3 tentativas de login consecutivas com o email "usuario_bloqueio@exemplo.com" e uma senha incorreta
    Então a conta do usuário "usuario_bloqueio@exemplo.com" deve ser bloqueada
    E todas as 3 tentativas devem exibir a mensagem "Senha inválida"
    Quando eu tento fazer login novamente com o email "usuario_bloqueio@exemplo.com" e a senha correta
    Então o sistema deve exibir uma mensagem indicando que a conta está bloqueada
```