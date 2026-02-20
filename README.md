# FLEXT Target Oracle

Singer Target para carga de dados em banco Oracle como destino final de pipeline.

Descricao oficial atual: "FLEXT Target Oracle - Singer Target for Oracle Database Data Loading".

## O que este projeto entrega

- Recebe stream Singer e persiste dados em Oracle.
- Padroniza escrita para cargas recorrentes.
- Apoia publicacao de datasets para consumo analitico e operacional.

## Contexto operacional

- Entrada: registros Singer de taps/orquestrador.
- Saida: dados gravados em tabelas Oracle.
- Dependencias: flext-db-oracle e conectividade com banco.

## Estado atual e risco de adocao

- Qualidade: **Alpha**
- Uso recomendado: **Nao produtivo**
- Nivel de estabilidade: em maturacao funcional e tecnica, sujeito a mudancas de contrato sem garantia de retrocompatibilidade.

## Diretriz para uso nesta fase

Aplicar este projeto somente em desenvolvimento, prova de conceito e homologacao controlada, com expectativa de ajustes frequentes ate maturidade de release.
