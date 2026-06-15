from graph.workflow import build_graph

graph = build_graph()

result = graph.invoke({
    "customer_query": "My vehicle app disconnects after login",
    "customer_id": "C001",
    "vehicle_id": "V001"
})

print(result)