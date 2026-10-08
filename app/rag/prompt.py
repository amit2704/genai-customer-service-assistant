SYSTEM_PROMPT = """You are an enterprise customer-service assistant.
Answer using only the supplied context.
If the context is insufficient, say you do not have enough information in the knowledge base.
Do not invent policies, prices, dates, or procedures.
Keep the answer concise and professional."""

def build_prompt(question, contexts):
    context_text = "\n\n".join(
        f"[Source: {x['source']} | Chunk: {x['chunk_id']}]\n{x['text']}"
        for x in contexts
    )
    return f"""{SYSTEM_PROMPT}

CONTEXT:
{context_text}

USER QUESTION:
{question}

ANSWER:"""
