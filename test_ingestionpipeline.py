from rag_pipeline.web_pipeline import fetch_web_content

query = "Birthday party venues in Hyderabad for 100 guests"
vector_store=fetch_web_content(query)
print("Documents stored:",vector_store._collection.count())