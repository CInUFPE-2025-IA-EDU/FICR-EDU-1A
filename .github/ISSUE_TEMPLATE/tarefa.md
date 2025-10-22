name: Tarefa
description: Tarefa de aluno (CSV → Issue)
title: "[Semana ${semana}] ${titulo}"
labels: ["tarefa"]
body:
  - type: markdown
    attributes:
      value: |
        **Descrição:** ${descricao}

        **Critérios de Aceite:**
        ${criterios}

        **Aluno (CodigoAluno):** ${codigo_aluno}
        **Squad:** ${squad}
