import requests
import pandas as pd
import base64

# === CONFIGURATION ===
SONAR_URL = "http://localhost:9000"  # your SonarQube URL
SONAR_TOKEN = "sonar token"  # your personal access token
PROJECT_KEY = "All your project key"  # optional: specific project key

# === AUTHENTICATION HEADER ===
token_bytes = f"{SONAR_TOKEN}:".encode("utf-8")
token_base64 = base64.b64encode(token_bytes).decode("utf-8")
HEADERS = {"Authorization": f"Basic {token_base64}"}

# === GET ALL PROJECTS ===
def get_all_projects():
    print("Fetching projects...")
    projects = []
    page = 1
    while True:
        url = f"{SONAR_URL}/api/projects/search?p={page}&ps=500"
        response = requests.get(url, headers=HEADERS)
        if response.status_code == 401:
            raise Exception("Unauthorized — check token permissions or header format.")
        response.raise_for_status()
        data = response.json()
        comps = data.get("components", [])
        if not comps:
            break
        projects.extend(comps)
        if len(comps) < 500:
            break
        page += 1
    return projects

# === GET ALL ISSUES ===
def get_all_issues(project_key):
    print(f"Fetching issues for: {project_key}")
    issues = []
    page = 1
    while True:
        url = f"{SONAR_URL}/api/issues/search?componentKeys={project_key}&p={page}&ps=500"
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        data = response.json()
        issues_page = data.get("issues", [])
        if not issues_page:
            break
        issues.extend(issues_page)
        if len(issues_page) < 500:
            break
        page += 1
    return issues

# === MAIN ===
if PROJECT_KEY:
    projects = [{"key": PROJECT_KEY, "name": PROJECT_KEY}]
else:
    projects = get_all_projects()

print(f"Found {len(projects)} projects")

all_data = []

for p in projects:
    key = p["key"]
    name = p.get("name", key)
    issues = get_all_issues(key)
    for i in issues:
        all_data.append({
            "Project": name,
            "Key": i.get("key"),
            "Rule": i.get("rule"),
            "Severity": i.get("severity"),
            "Component": i.get("component"),
            "Message": i.get("message"),
            "Line": i.get("line"),
            "Status": i.get("status"),
            "Type": i.get("type"),
        })

if not all_data:
    print("No issues found or insufficient permissions.")
else:
    df = pd.DataFrame(all_data)
    df.to_excel("sonarqube_issues.xlsx", index=False)
    print("Exported to sonarqube_issues.xlsx")
