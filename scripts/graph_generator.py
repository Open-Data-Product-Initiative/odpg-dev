import yaml
import json
from pathlib import Path


def load_graph(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return yaml.safe_load(file)


def validate_graph(graph):
    required_root_fields = ["schema", "version", "kind", "id", "name", "nodes", "edges"]

    for field in required_root_fields:
        if field not in graph:
            raise ValueError(f"Missing required field: {field}")

    node_ids = set()

    for node in graph["nodes"]:
        for field in ["id", "type", "$ref"]:
            if field not in node:
                raise ValueError(f"Missing required node field: {field}")

        node_ids.add(node["id"])

    for edge in graph["edges"]:
        for field in ["from", "to", "type", "confidence"]:
            if field not in edge:
                raise ValueError(f"Missing required edge field: {field}")

        if edge["from"] not in node_ids:
            raise ValueError(f"Invalid edge source: {edge['from']}")

        if edge["to"] not in node_ids:
            raise ValueError(f"Invalid edge target: {edge['to']}")

    return True


def build_html(graph):
    graph_name = graph["name"].get("en") or next(iter(graph["name"].values()))

    nodes = [
        {
            "id": node["id"],
            "label": node["id"],
            "group": node["type"],
            "title": f"{node['type']}<br>{node['$ref']}"
        }
        for node in graph["nodes"]
    ]

    edges = [
        {
            "from": edge["from"],
            "to": edge["to"],
            "label": edge["type"],
            "arrows": "to"
        }
        for edge in graph["edges"]
    ]

    return f"""
<!DOCTYPE html>
<html>
<head>
  <title>{graph_name}</title>

  <script src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>

  <style>
    body {{
      margin: 0;
      font-family: Arial;
    }}

    #graph {{
      width: 100vw;
      height: 100vh;
      background: #f8fafc;
    }}
  </style>
</head>

<body>

<div id="graph"></div>

<script>

const nodes = new vis.DataSet({json.dumps(nodes)});
const edges = new vis.DataSet({json.dumps(edges)});

const container = document.getElementById("graph");

const data = {{
  nodes: nodes,
  edges: edges
}};

const options = {{
  physics: {{
    stabilization: true
  }},
  interaction: {{
    hover: true
  }}
}};

new vis.Network(container, data, options);

</script>

</body>
</html>
"""


def generate_graph_explorer(input_file, output_file):

    graph = load_graph(input_file)

    validate_graph(graph)

    html = build_html(graph)

    Path(output_file).write_text(html, encoding="utf-8")

    print(f"Graph Explorer generated: {output_file}")


if __name__ == "__main__":

    generate_graph_explorer(
        input_file="graph.yaml",
        output_file="graph-explorer.html"
    )
