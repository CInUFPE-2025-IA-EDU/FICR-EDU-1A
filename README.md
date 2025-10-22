# FICR-EDU-1A

Repositório da disciplina **FICR-EDU-1A**.

## Objetivo
- Centralizar tarefas dos alunos via *Issues*.
- Padronizar *PRs* e revisão por pares.
- Automatizar a criação de *issues* a partir de uma planilha CSV.

## Como usar (resumo)
1. Faça upload deste repositório para o GitHub (organização sugerida: **CInUFPE-2025-IA-EDU**).
2. Vá em **Actions → Seed Issues from CSV → Run workflow**.
3. Opcionalmente, edite `config/students.yaml` para mapear o `CodigoAluno` ao login do GitHub.
4. O workflow vai:
   - Ler `tasks/requisitos_autopecas_formulario_html_css_tarefas.csv`,
   - Criar *issues* para cada linha, com labels de **Semana**, **Squad** e **Aluno**,
   - Atribuir a issue ao aluno correspondente (se encontrado em `students.yaml`).

## Estrutura
```
FICR-EDU-1A/
  .github/
    ISSUE_TEMPLATE/
    workflows/
  tools/
  tasks/
  config/
  src/
  docs/
```
