from transformers import AutoModelForPreTraining, AutoTokenizer
from normalizer import normalize # pip install git+https://github.com/csebuetnlp/normalizer
import torch

def perform_bangla_sentiment(text):
    model = AutoModelForPreTraining.from_pretrained("csebuetnlp/banglabert")
    tokenizer = AutoTokenizer.from_pretrained("csebuetnlp/banglabert")

    # Process the text
    processed_text = normalize(text)

    # Extract text only
    processed_tokens = tokenizer.tokenize(processed_text)
    processed_inputs = tokenizer.encode(processed_text, return_tensors="pt")
    discriminator_outputs = model(processed_inputs).logits
    predictions = torch.round((torch.sign(discriminator_outputs) + 1) / 2)

    [print("%7s" % token, end="") for token in processed_tokens]
    print("\n" + "-" * 50)
    [print("%7s" % int(prediction), end="") for prediction in predictions.squeeze().tolist()[1:-1]]
    print("\n" + "-" * 50)

    # Return output
    return predictions