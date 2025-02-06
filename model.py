import torch
from transformers import RobertaTokenizer, RobertaForSequenceClassification, pipeline, AutoTokenizer
from db import insert_data

# create huggingface pipeline for model
classifier = pipeline(
            "text-classification",
            model='vectara/hallucination_evaluation_model',
            tokenizer=AutoTokenizer.from_pretrained('google/flan-t5-base'),
            trust_remote_code=True
        )


def vectara(str):
    try:
        pre, hypo = str.split(".",1) #splits the string based on first encountered "."
        if pre=="" or hypo =="":
            raise Exception        #raise exception for edge cases
    except ValueError:
        return None  

    #creating prompt for model
    prompt = "<pad> Determine if the hypothesis is true given the premise?\n\nPremise: {text1}\n\nHypothesis: {text2}"
    input_pairs = [prompt.format(text1=pre, text2=hypo)]

    full_scores = classifier(input_pairs, top_k=None) # List[List[Dict[str, float]]]

    # Optional: Extract the scores for the 'consistent' label
    simple_scores = [score_dict['score'] for score_for_both_labels in full_scores for score_dict in score_for_both_labels if score_dict['label'] == 'consistent']

    return simple_scores




def toxic(str):
    model = RobertaForSequenceClassification.from_pretrained('s-nlp/roberta_toxicity_classifier') #calls model from huggning face
    tokenizer = RobertaTokenizer.from_pretrained('s-nlp/roberta_toxicity_classifier') #takes an input and coverts to embedding vector
    batch = tokenizer.encode(str, return_tensors="pt") #how to send an array of string?

    with torch.no_grad():           #disables gradient calculation since we are not training model
        logits = model(batch).logits  

    predicted_class_id = logits.argmax().item() #this returns the class with higher value, # idx 0 for neutral, idx 1 for toxic
    return predicted_class_id


def call_llm(string):
    toxic_out = toxic(string)
    vectara_out = vectara(string)
    if vectara_out is not None:
        data = {                                   #converts the output to json format so it can be easily handeled by API and frontend
            "Received text:": string,
            "Vectara": vectara_out[0],
            "Toxicity": toxic_out
            }
        insert_data(string,toxic_out,vectara_out) #insert data into DB
        return data
    else:
        return {"error": "Invalid input format. please enter in following format 'sentence1,sentence2' where both sentence are separated by comma."}