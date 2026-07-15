from transformers import pipeline

pipe = pipeline(task="text-generation", model="Qwen/Qwen2.5-1.5B")
response = pipe("the secret to baking a really good cake is ")

print("\n\n\n\n")
print(response[0]['generated_text'])
