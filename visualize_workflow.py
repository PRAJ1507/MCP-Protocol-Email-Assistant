from langgraph_flow import workflow

def visualize_workflow():
    nodes = list(workflow.nodes.keys())
    edges = list(workflow.edges)
    print("Nodes:", nodes)
    print("Edges:")
    for src, tgt in edges:
        print(f"  {src} -> {tgt}")

if __name__ == "__main__":
    visualize_workflow()