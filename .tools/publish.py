"""Publish the AromaPacifico board to GitHub: repos, labels, milestones, issues and Project.

Usage: python3 publish.py [--dry-run]
Re-running is safe: existing labels, milestones, issues (by title) and fields are reused.
"""
import json
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from issues import ISSUES, LABELS, MILESTONES  # noqa: E402

ORG = "aromapacifico-platform"
REPO = f"{ORG}/planning"
PROJECT_TITLE = "Kanban Board"
DRY = "--dry-run" in sys.argv

STATUS = ["Backlog", "Ready", "In progress", "In review", "Done"]
FIELDS = {
    "Fase": [f"fase-{n}" for n in range(0, 8)],
    "Entregable": ["decisiones-base", "arquitectura", "iac", "costos", "cambio",
                   "sustentacion", "diseno", "transversal"],
    "Prioridad": ["Alta", "Media", "Baja"],
}


def gh(*args, input=None, check=True):
    if DRY and args[0] not in ("api",) and not args[0].startswith("issue list"):
        print("DRY gh", " ".join(args)[:160])
    res = subprocess.run(["gh", *args], input=input, capture_output=True, text=True)
    if check and res.returncode != 0:
        raise SystemExit(f"gh {' '.join(args)[:200]}\n{res.stderr}")
    return res.stdout


def graphql(query, **variables):
    args = ["api", "graphql", "-f", f"query={query}"]
    for k, v in variables.items():
        args += ["-F" if isinstance(v, int) else "-f", f"{k}={v}"]
    return json.loads(gh(*args))["data"]


def render(issue, numbers):
    deps = "\n".join(f"- Depende de #{numbers[d]}" for d in issue["deps"]) or \
        "Ninguna (puede iniciarse de inmediato)."
    criterios = "\n".join(f"- [ ] {c}" for c in issue["criterios"])
    return f"""## Historia de usuario
{issue['historia']}

## Contexto
{issue['contexto']}

## Qué construir
{issue['construir']}

**Entregable:** {issue['entregable_txt']}

## Datos del caso
{issue['datos']}

## Criterios de aceptación
{criterios}

## Dependencias
{deps}

## Cobertura
{issue['cobertura']}
"""


def ensure_labels():
    existing = {l["name"] for l in json.loads(gh("label", "list", "-R", REPO, "--limit", "200",
                                                  "--json", "name"))}
    for name, (desc, color) in LABELS.items():
        if name not in existing and not DRY:
            gh("label", "create", name, "-R", REPO, "-d", desc, "-c", color)


def ensure_milestones():
    existing = {m["title"]: m["number"] for m in json.loads(
        gh("api", f"repos/{REPO}/milestones?state=all&per_page=100"))}
    for title in MILESTONES.values():
        if title not in existing and not DRY:
            gh("api", f"repos/{REPO}/milestones", "-f", f"title={title}")


def ensure_issues():
    existing = {i["title"]: i["number"] for i in json.loads(
        gh("issue", "list", "-R", REPO, "--state", "all", "--limit", "500",
           "--json", "title,number"))}
    numbers = {}
    for issue in ISSUES:
        if issue["title"] in existing:
            numbers[issue["key"]] = existing[issue["title"]]
            continue
        labels = ",".join([issue["fase"], issue["entregable"], *issue["labels"]])
        if DRY:
            numbers[issue["key"]] = 1000 + len(numbers)
            print(render(issue, numbers)[:0] or f"DRY issue {issue['title']}")
            continue
        url = gh("issue", "create", "-R", REPO, "--title", issue["title"],
                 "--body", render(issue, numbers), "--label", labels,
                 "--milestone", MILESTONES[issue["fase"]]).strip()
        numbers[issue["key"]] = int(url.rsplit("/", 1)[1])
        print(f"#{numbers[issue['key']]} {issue['title']}")
    return numbers


def ensure_project():
    projects = json.loads(gh("project", "list", "--owner", ORG, "--format", "json"))["projects"]
    project = next((p for p in projects if p["title"] == PROJECT_TITLE), None)
    if project is None:
        project = json.loads(gh("project", "create", "--owner", ORG, "--title", PROJECT_TITLE,
                                "--format", "json"))
    gh("project", "link", str(project["number"]), "--owner", ORG, "--repo", REPO, check=False)
    return project


def project_fields(number):
    return {f["name"]: f for f in json.loads(
        gh("project", "field-list", str(number), "--owner", ORG, "--format", "json",
           "--limit", "100"))["fields"]}


def ensure_fields(project):
    fields = project_fields(project["number"])
    status = fields["Status"]
    if [o["name"] for o in status.get("options", [])] != STATUS:
        opts = ", ".join('{name: "%s", color: GRAY, description: ""}' % s for s in STATUS)
        graphql("mutation($id: ID!) { updateProjectV2Field(input: {fieldId: $id, "
                "singleSelectOptions: [%s]}) { clientMutationId } }" % opts, id=status["id"])
    for name, options in FIELDS.items():
        if name not in fields:
            gh("project", "field-create", str(project["number"]), "--owner", ORG, "--name", name,
               "--data-type", "SINGLE_SELECT", "--single-select-options", ",".join(options))
    return project_fields(project["number"])


def set_select(project_id, item_id, field, value):
    option = next(o["id"] for o in field["options"] if o["name"] == value)
    gh("project", "item-edit", "--project-id", project_id, "--id", item_id,
       "--field-id", field["id"], "--single-select-option-id", option)


def main():
    ensure_labels()
    ensure_milestones()
    numbers = ensure_issues()
    if DRY:
        print(f"DRY: {len(numbers)} issues")
        return
    project = ensure_project()
    fields = ensure_fields(project)
    items = {i["content"]["number"]: i["id"] for i in json.loads(
        gh("project", "item-list", str(project["number"]), "--owner", ORG, "--format", "json",
           "--limit", "500"))["items"] if i.get("content", {}).get("number")}
    for issue in ISSUES:
        n = numbers[issue["key"]]
        item_id = items.get(n) or json.loads(gh(
            "project", "item-add", str(project["number"]), "--owner", ORG,
            "--url", f"https://github.com/{REPO}/issues/{n}", "--format", "json"))["id"]
        set_select(project["id"], item_id, fields["Status"],
                   "Ready" if not issue["deps"] else "Backlog")
        set_select(project["id"], item_id, fields["Fase"], issue["fase"])
        set_select(project["id"], item_id, fields["Entregable"], issue["entregable"])
        set_select(project["id"], item_id, fields["Prioridad"], issue["prioridad"])
    print(f"Project: https://github.com/orgs/{ORG}/projects/{project['number']}")


if __name__ == "__main__":
    main()
