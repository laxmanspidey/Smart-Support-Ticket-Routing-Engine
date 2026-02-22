import time
from sentence_transformers import SentenceTransformer, util
from services.transformer_ml import predict_category
from services.classifier import classify_ticket  # Your Milestone 1 fallback

print("Loading Sentence Embedding model for Deduplication...")
embedder = SentenceTransformer('all-MiniLM-L6-v2')

# In-memory stores for Milestone 3 state
ticket_history = []  # Stores tuples of (timestamp, embedding)

# Stateful registry of agents with Skill Vectors and capacity
AGENT_REGISTRY = [
    {"name": "Agent Alice", "skills": {"Technical": 0.9, "Billing": 0.1, "Legal": 0.0}, "capacity": 5},
    {"name": "Agent Bob", "skills": {"Technical": 0.2, "Billing": 0.8, "Legal": 0.0}, "capacity": 3},
    {"name": "Agent Charlie", "skills": {"Technical": 0.1, "Billing": 0.1, "Legal": 0.9}, "capacity": 4},
]

def check_ticket_storm(text: str) -> bool:
    """Calculates Cosine Similarity to detect flash-floods."""
    global ticket_history
    now = time.time()
    
    # 1. Clean up old tickets (keep only the last 5 minutes / 300 seconds)
    ticket_history = [t for t in ticket_history if now - t[0] <= 300]
    
    # 2. Generate embedding for the new ticket
    new_embedding = embedder.encode(text, convert_to_tensor=True)
    
    # 3. Calculate similarities
    similar_count = 0
    for _, old_embedding in ticket_history:
        similarity = util.cos_sim(new_embedding, old_embedding).item()
        if similarity > 0.9:
            similar_count += 1
            
    # 4. Store the new ticket
    ticket_history.append((now, new_embedding))
    
    # 5. Check threshold (> 10 similar tickets)
    return similar_count >= 10

def get_category_with_circuit_breaker(text: str) -> str:
    """Fails over to M1 model if Transformer latency > 500ms."""
    start_time = time.time()
    
    # Run the heavy Transformer model
    category = predict_category(text)
    
    latency_ms = (time.time() - start_time) * 1000
    
    if latency_ms > 500:
        print(f"⚠️ CIRCUIT BREAKER TRIPPED! Latency {latency_ms:.2f}ms > 500ms. Using M1 Fallback.")
        # Fallback to the regex baseline
        return classify_ticket(text) 
    
    return category

def route_to_best_agent(category: str) -> str:
    """Constraint Optimization based on skill match and capacity."""
    best_agent = None
    max_score = -1.0
    
    for agent in AGENT_REGISTRY:
        if agent["capacity"] > 0:
            score = agent["skills"].get(category, 0.0)
            if score > max_score:
                max_score = score
                best_agent = agent
                
    if best_agent:
        best_agent["capacity"] -= 1  # Reserve their capacity
        return best_agent["name"]
    return "Overflow Queue (No Agents Available)"