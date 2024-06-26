from api.chains.qa_chain_with_rag import create_llm_finetun_chain
from api.chains.off_topic_chain import create_off_topic_chain
from api.chains.classification_chain import create_classification_chain
from langchain_core.runnables import (
    RunnableBranch,
    RunnableLambda, 
    
)
from utils import custom_load_memory
from operator import itemgetter

def init_full_chain(llm):
    qa_chain = create_llm_finetun_chain(llm)
    off_topic_chain = create_off_topic_chain(llm)
    classification_chain = create_classification_chain(llm)
    
    full_chain = (
        {"category": classification_chain,
         "question": itemgetter("question"),
         "user_settings": itemgetter("user_settings"),
         "topics": itemgetter("topics"),
         "memory": {"memory": itemgetter("memory") | RunnableLambda(custom_load_memory)},
         } | RunnableBranch(
             (lambda x: "qa" in x['category'].lower(), qa_chain),
             (lambda x: "other" in x['category'].lower(), off_topic_chain),
             off_topic_chain
         ) 
    )
    
    return full_chain
    
    
    