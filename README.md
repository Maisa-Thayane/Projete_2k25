# ANTLION – Projeto Acadêmico de Cybersecurity

O **ANTLION** é um projeto acadêmico de **cybersecurity** que simula um sistema de autenticação protegido por múltiplas camadas de segurança, com foco na **detecção, análise e contenção de comportamentos maliciosos** em ambientes web.

Desenvolvido para apresentação acadêmica e feira de projetos, o ANTLION demonstra, de forma didática, como ataques comuns podem ser identificados, mitigados e estudados, sem a pretensão de substituir soluções profissionais de segurança.

---

## Apresentação do Projeto

Ao acessar o sistema, o possível invasor passa por diversas camadas de proteção aplicadas em sequência. Inicialmente, há um **limite de tentativas de senha**, reduzindo ataques por força bruta (tentativa e erro). Em seguida, o endereço IP é analisado por meio de uma **API externa**, verificando se há indícios de comportamento malicioso.

Caso essas etapas sejam superadas, o sistema exige uma **autenticação em dois fatores (2FA)**, baseada no envio de um código de confirmação por e-mail. Paralelamente, o sistema avalia padrões de uso, como **cliques na interface e velocidade de interação**, com o objetivo de identificar possíveis bots automatizados.

Sempre que qualquer uma dessas defesas detecta uma anomalia, o usuário é redirecionado para um **honeypot**, ambiente controlado onde o comportamento do invasor pode ser observado e analisado, contribuindo para o aprendizado sobre métodos de ataque.

As informações dos usuários legítimos são tratadas com cuidado, sendo protegidas por **múltiplas camadas de criptografia**, aplicadas de forma contínua ao longo do fluxo do sistema.

---

## Objetivo

* Simular mecanismos básicos de segurança utilizados em sistemas reais
* Demonstrar o funcionamento de múltiplas camadas de defesa
* Estudar e observar comportamentos suspeitos por meio de honeypot
* Consolidar conhecimentos iniciais em cybersecurity de forma prática

---

## Tecnologias Utilizadas

* **HTML5**
* **Python**
* Integração com **API externa** para análise de IP
* Armazenamento local para fins educacionais (SQLite)

---

## Observação Importante

Este projeto possui **finalidade exclusivamente educacional**. As técnicas apresentadas não devem ser consideradas suficientes para ambientes de produção. O ANTLION tem como propósito demonstrar conceitos, lógica de segurança e postura responsável no estudo de cybersecurity em nível iniciante.

---

## Autoria

Projeto desenvolvido em colaboração por:


* **Maísa Thayane dos Santos**
* *(Adicionar nome do(a) colega 1)*
* *(Adicionar nome do(a) colega 2)*
* *(Adicionar nome do(a) colega 3)*
