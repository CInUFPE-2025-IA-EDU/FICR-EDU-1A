#!/usr/bin/env python3
import argparse
import csv
import os
import sys
from github import Github
import yaml

def ensure_label(repo, name, color="5E81AC", description=""):
    try:
        return repo.get_label(name)
    except:
        return repo.create_label(name=name, color=color, description=description)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", required=True, help="owner/repo")
    parser.add_argument("--token", required=True, help="GitHub token")
    parser.add_argument("--csv", required=True, help="path to tasks CSV")
    parser.add_argument("--students", required=False, default=None, help="students.yaml mapping")
    parser.add_argument("--dry-run", default="false", help="true/false")
    args = parser.parse_args()

    dry_run = str(args.dry_run).lower() == "true"

    g = Github(args.token)
    repo = g.get_repo(args.repo)

    mapping = {}
    if args.students and os.path.exists(args.students):
        with open(args.students, "r", encoding="utf-8") as f:
            y = yaml.safe_load(f) or {}
            mapping = (y.get("mappings") or {})

    with open(args.csv, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        required_cols = {"Semana","Titulo","Descricao","Criterios","CodigoAluno","Squad"}
        if not required_cols.issubset(set([c.strip() for c in reader.fieldnames])):
            print(f"[ERRO] CSV precisa das colunas: {required_cols}", file=sys.stderr)
            sys.exit(1)

        # Ensure base labels
        ensure_label(repo, "tarefa", "2E7D32", "Tarefas de alunos")
        ensure_label(repo, "bug", "D73A4A", "Reporte de bug")

        for row in reader:
            semana = row.get("Semana","").strip()
            titulo = row.get("Titulo","").strip()
            descricao = row.get("Descricao","").strip()
            criterios = row.get("Criterios","").strip()
            codigo_aluno = row.get("CodigoAluno","").strip()
            squad = row.get("Squad","").strip()

            issue_title = f"[Semana {semana}] {titulo}".strip()
            body = (
                f"**Descrição**\n{descricao}\n\n"
                f"**Critérios de Aceite**\n{criterios}\n\n"
                f"**Aluno (CodigoAluno):** {codigo_aluno}\n"
                f"**Squad:** {squad}\n"
            )

            # dynamic labels
            labels = ["tarefa"]
            if semana:
                labels.append(f"Semana:{semana}")
            if squad:
                labels.append(f"Squad:{squad}")
            if codigo_aluno:
                labels.append(f"Aluno:{codigo_aluno}")

            # ensure labels exist
            for lb in labels[1:]:  # skip 'tarefa' (already ensured)
                try:
                    ensure_label(repo, lb, "6E5494")
                except Exception as e:
                    print(f"[WARN] Não foi possível criar label {lb}: {e}")

            assignees = []
            # try map CodigoAluno -> login
            if codigo_aluno and mapping:
                entry = mapping.get(str(codigo_aluno))
                if entry and isinstance(entry, dict):
                    login = entry.get("login")
                    if login:
                        assignees = [login]

            print(f"→ {'DRY-RUN: ' if dry_run else ''}Criando issue: {issue_title} | assignees={assignees} | labels={labels}")
            if not dry_run:
                try:
                    repo.create_issue(
                        title=issue_title,
                        body=body,
                        labels=labels,
                        assignees=assignees
                    )
                except Exception as e:
                    print(f"[ERRO] Falha ao criar issue '{issue_title}': {e}", file=sys.stderr)

if __name__ == "__main__":
    main()
