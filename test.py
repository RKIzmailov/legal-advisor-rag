import pandas as pd
import requests

df = pd.read_csv("data/ground_truth_data.csv")
question = df.sample(n=1).iloc[0]['question']
question = 'During what period a buyer must return a product within the EAEU if the buyer cannot pay for the product?'

print("question: ", question)

url = "http://localhost:5000/ask"

data = {"question": question}

response = requests.post(url, json=data)
print(response.json())
