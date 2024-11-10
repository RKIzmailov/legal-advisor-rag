# Legal Advisor on Kyrgyz Republic legislation

## 1.1. Problem

Accessing legal information can be a daunting and time-consuming task, especially when dealing with complex legal documents and navigating through various codes and statutes. In the context of the Kyrgyz Republic, understanding the specifics of the law often requires professional legal assistance, which may not always be accessible or affordable for everyone. The average citizen, lawyer, or government official may struggle to quickly find relevant legal information without a deep understanding of where and how to search through legislative documents.

## 1.2. Project Description

The **Legal Advisor** application is designed to solve this problem by providing an easy-to-use, AI-powered legal consultation tool. Built using Retrieval-Augmented Generation (RAG) technology, the application allows users to ask legal questions related to Kyrgyz Republic legislation and receive accurate, law-referenced answers. The system queries a dataset containing Kyrgyz Republic’s key legal codes, such as the Water Code, Civil Code, Family Code, and others. The responses include specific references to the law and its corresponding articles, making legal information more accessible, efficient, and reliable.

By simplifying access to legal knowledge, **Legal Advisor** empowers users to understand their legal rights and obligations without needing professional legal assistance for every inquiry.


**Technologies**

  - `Python 3.12`
  - `Llama-index` as a RAG framework
  - `Weaviate` as a Vector database
  - `OpenAI` as an LLM
  - `Flask` as the API interface


## 1.3. Data Description

The system queries a dataset containing Kyrgyz Republic’s key legal codes. The document are in Russian, but you can interact with tem in English or in Russian at your convinience.

- Water Code of the Kyrgyz Republic
- Civil Code of the Kyrgyz Republic Part I
- Civil Code of the Kyrgyz Republic Part II
- Civil Procedure Code of the Kyrgyz Republic
- Land Code of the Kyrgyz Republic
- Code of the Kyrgyz Republic on Offenses
- Tax Code of the Kyrgyz Republic
- Family Code of the Kyrgyz Republic
- Criminal Procedure Code of the Kyrgyz Republic
- Criminal Code of the Kyrgyz Republic

# 2. Running and using the application

## 2.1. Environment preparation

1. Create a folder and clone the GitHub repository.

2. Make sure you have `pipenv` installed:

    ```bash
    pip install pipenv
    ```

3. Install the app dependencies:

    ```bash
    pipenv install --dev
    ```

4. Rename the `.env_template` file to `.env`.

5. The application uses OpenAI, so you need an OpenAI API key. Add your `OPENAI_KEY` to the `.env` file.

6. The application uses a Weaviate vector database. Weaviate provides a 2-week free trial period, so you can create a Weaviate account and obtain:
    - `REST Endpoint`
    - `Weaviate Admin API key`
    - `Weaviate ReadOnly API key`

    This information should also be added to the `.env` file.

7. Activate the virtual environment:

    ```bash
    pipenv shell
    ```

## 2.2. Laws Database Configuration

The database needs to be initialized before the application starts for the first time.

Laws are situated in the `data/laws` folder. You can add other laws in .txt format if you need **Legal Advisor** to provide consultations on your laws.

1. Check the `data/laws` folder and ensure it consists of the required laws.

2. Run the `./app/db_weaviate_prep.py` file:

    ```bash
    python app/db_weaviate_prep.py
    ```

## 2.3. Language Configuration

You can adjust the language of responses by changing this parameter in the `config.yaml` file.

Right now you can use English or Russian. Configure `config.yaml` file accordingly.


## 2.4. Running the Application

Flask is used for serving the application as an API.

To run the application:

```bash
python app/app.py
```

## 2.5. Using the Application

### 2.5.1. Using the Interactive Tool

a) The easiest way to interact with the **Legal Advisor** is to run `cli.py` with a simple terminal-format interactive tool:

``` bash
python cli.py
```
The application will prompt you to ask a question, allowing you to interact with it.

```bash
Welcome to the interactive question-answering app!
You can exit the program at any time when prompted.
? Enter your question:
```

After that, the application will provide the answer and ask for feedback.

```bash
? Enter your question: What action does the presiding judge take after reviewing the objections, and how are these handled in relation to the court session protocol?

Answer: After considering the objections, the presiding judge takes the following actions according to the Criminal Procedure Code of the Kyrgyz Republic, Article 309:

1. The presiding judge issues a ruling to confirm the correctness of the objections or to reject them.
2. The objections to the trial protocol and the ruling of the presiding judge are attached to the trial protocol.

These actions are documented in the trial protocol, ensuring transparency and proper record-keeping of the judicial proceedings.

? How would you rate this response? (Use arrow keys)
» +1 (Positive)
-1 (Negative)
Pass (Skip feedback)
```

b) You can also run `cli.py` in the form of automatically choosing a random question from `ground_truth_data.csv`. Just pass `--random` as a parameter.

``` bash
python cli.py --random
```

In this case, the output will look like:

```bash
Welcome to the interactive question-answering app!
You can exit the program at any time when prompted.

Random question: Are there any construction activities allowed on particularly valuable agricultural lands, and if so, what are they?

Answer: Construction on particularly valuable agricultural lands is generally not permitted. However, Article 74 of the Land Code of the Kyrgyz Republic specifies that the only exceptions allowed are for the construction of hydraulic engineering structures, greenhouses, and drip irrigation systems on irrigated fields. 

? How would you rate this response? (Use arrow keys)
» +1 (Positive)
-1 (Negative)
Pass (Skip feedback)
```

### 2.5.2. You can also use invoke / curl

Open a new terminal and run the following commands:

- To ask the question if you use **PowerShell** (change question if needed):

    ```bash
    $response = Invoke-WebRequest -Uri http://localhost:5000/ask `
    -Method POST `
    -ContentType "application/json" `
    -Body '{"question": "What evidence is required for a person to be formally charged as an accused?"}' `
    -UseBasicParsing

    # Output the Content in JSON format
    Write-Output $response.Content
    ```

- if you use **Linux**:

    ```bash
    curl -X POST http://localhost:5000/ask \
    -H "Content-Type: application/json" \
    -d '{"question": "What evidence is required for a person to be formally charged as an accused?"}'
    ```

    The answer will look like:


    ```bash
    {
    "conversation_id": "a9992387-e662-43ad-930f-f3cb983ffdc6",
    "question": "What evidence is required for a person to be formally charged as an accused?",
    "result": "To officially hold a person accountable as an accused, sufficient evidence indicating that the person committed a crime is required, as stated in Article 240 of the Criminal Procedure Code of the Kyrgyz Republic. The investigator issues a motivated decision to charge the individual based on this evidence."
    }
    ```
- To provide feedback if you use **PowerShell** (change the conversation ID)

    ```bash
    $ID = "a9992387-e662-43ad-930f-f3cb983ffdc6"
    $FEEDBACK = 1
    $URL = "http://localhost:5000"

    $FEEDBACK_DATA = @{
        conversation_id = $ID
        feedback = $FEEDBACK
    } | ConvertTo-Json

    $response = Invoke-WebRequest -Uri "$URL/feedback" `
    -Method POST `
    -ContentType "application/json" `
    -Body $FEEDBACK_DATA

    # Output the Content in JSON format
    Write-Output $response.Content
    ```

- if you use **Linux**:

    ```bash
    ID="a9992387-e662-43ad-930f-f3cb983ffdc6"
    FEEDBACK=1
    URL="http://localhost:5000"
    FEEDBACK_DATA='{
    "conversation_id": "'${ID}'",
    "feedback": '${FEEDBACK}'
    }'

    curl -X POST "${URL}/feedback" \
    -H "Content-Type: application/json" \
    -d "${FEEDBACK_DATA}"
    ```

    The answer will look like:

    ```bash
    {
        "conversation_id": "a9992387-e662-43ad-930f-f3cb983ffdc6",
        "feedback": 1,
        "message": "Feedback received. Thank you!"
    }
    ```

### 2.5.3. Using `request`

You can also interact with the application by using `request`

```bash
import pandas as pd
import requests

question = "What evidence is required for a person to be formally charged as an accused?"

url = "http://localhost:5000/ask"

data = {"question": question}

response = requests.post(url, json=data)
print(response.json())
```

If you run the `test.py` file, it will take the random question in English from `ground_truth_data.csv` and provide the answer.

```bash
python test.py
```
The answer will look like:

```bash
{
'conversation_id': '482c9d48-c0d3-4d30-a2cb-dab0e0f6a880', 
'question': 'What role does the court play in guiding the civil process according to the law?', 
'result': 'The court plays a crucial role in managing the civil process according to the law. As stated in Article 10 of the Civil Procedure Code of the Kyrgyz Republic, justice in civil cases is carried out based on the adversarial nature and equality of the parties. The court, while maintaining objectivity and impartiality, directs the process, clarifies the rights and obligations of the parties involved, and creates conditions for a comprehensive and complete examination of evidence, establishment of facts, and correct application of the law in resolving civil cases.'
}
```

Have fun!

# 3. Experiments

## 3.1. RAG flow

For experiments, I used Visual Studio Code.

The notebook with experiments is located in the [law-rag-test.ipynb](/experiments/law-rag-test.ipynb) file.

### 3.2. Retrieval evaluation

I evaluated 3 different retrieval methods and different `alpha` values for `hybrid search`:

- alpha values from 0.1 to 1.0
- user query in English *(to test how the retriever will search for documents in a language different from the user query language)*;
- user query in English, but translated to Russian on the fly *(to test how retriever will perform search of the documents which are on the same language as users query)*;
- reranker `colbert_reranker`

Here are the results:

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>alpha</th>
      <th>hit_rate</th>
      <th>mrr</th>
      <th>hit_rate_ru_query</th>
      <th>mrr_ru_query</th>
      <th>hit_rate_rerank</th>
      <th>mrr_rerank</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>0.1</td>
      <td>0.626667</td>
      <td>0.382622</td>
      <td>0.686667</td>
      <td>0.484405</td>
      <td>0.686667</td>
      <td>0.484405</td>
    </tr>
    <tr>
      <th>1</th>
      <td>0.2</td>
      <td>0.626667</td>
      <td>0.382622</td>
      <td>0.720000</td>
      <td>0.516323</td>
      <td>0.720000</td>
      <td>0.516323</td>
    </tr>
    <tr>
      <th>2</th>
      <td>0.3</td>
      <td>0.626667</td>
      <td>0.382622</td>
      <td>0.753333</td>
      <td>0.546304</td>
      <td>0.753333</td>
      <td>0.546304</td>
    </tr>
    <tr>
      <th>3</th>
      <td>0.4</td>
      <td>0.626667</td>
      <td>0.382622</td>
      <td>0.793333</td>
      <td>0.563156</td>
      <td>0.793333</td>
      <td>0.563156</td>
    </tr>
    <tr>
      <th>4</th>
      <td>0.5</td>
      <td>0.633333</td>
      <td>0.389288</td>
      <td>0.806667</td>
      <td>0.564524</td>
      <td>0.806667</td>
      <td>0.564524</td>
    </tr>
    <tr>
      <th>5</th>
      <td>0.6</td>
      <td>0.633333</td>
      <td>0.389288</td>
      <td>0.800000</td>
      <td>0.548487</td>
      <td>0.800000</td>
      <td>0.548487</td>
    </tr>
    <tr>
      <th>6</th>
      <td>0.7</td>
      <td>0.640000</td>
      <td>0.389955</td>
      <td>0.766667</td>
      <td>0.513161</td>
      <td>0.766667</td>
      <td>0.513161</td>
    </tr>
    <tr>
      <th>7</th>
      <td>0.8</td>
      <td>0.640000</td>
      <td>0.390122</td>
      <td>0.726667</td>
      <td>0.487958</td>
      <td>0.726667</td>
      <td>0.487958</td>
    </tr>
    <tr>
      <th>8</th>
      <td>0.9</td>
      <td>0.640000</td>
      <td>0.390622</td>
      <td>0.666667</td>
      <td>0.438357</td>
      <td>0.666667</td>
      <td>0.438357</td>
    </tr>
    <tr>
      <th>9</th>
      <td>1.0</td>
      <td>0.640000</td>
      <td>0.390955</td>
      <td>0.633333</td>
      <td>0.389579</td>
      <td>0.633333</td>
      <td>0.389579</td>
    </tr>
  </tbody>
</table>
</div>


The best results are provided by retriever that perform search of the documents which are on the same language as users query. So if users query is in English it is translated to Russian on the fly.

### 3.3. RAG evaluation

I have used `gpt-4o-mini` as an LLM agent and evaluated 3 different promts:
- simple prompt without examples;
- prompt with examples;
- prompt that activates the `chain-of-thought` behavior of LLM.

The metric is `LLM-as-a-Judge` that evaluates the answer in terms of relevance to the question and to the ground truth context.

Here are the results:

<div>
  <style scoped>
      .dataframe tbody tr th:only-of-type {
          vertical-align: middle;
      }
  </style>
<table class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th></th>
      <th>count</th>
      <th>count_norm</th>
    </tr>
    <tr>
      <th>template_name</th>
      <th>relevance</th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th rowspan="3" valign="top">promt_template_1</th>
      <th>NON_RELEVANT</th>
      <td style="text-align: center;">8</td>
      <td style="text-align: center;">1.8%</td>
    </tr>
    <tr>
      <th>PARTLY_RELEVANT</th>
      <td style="text-align: center;">44</td>
      <td style="text-align: center;">9.8%</td>
    </tr>
    <tr>
      <th>RELEVANT</th>
      <td style="text-align: center;">98</td>
      <td style="text-align: center;">21.8%</td>
    </tr>
    <tr>
      <th rowspan="3" valign="top">promt_template_2</th>
      <th>NON_RELEVANT</th>
      <td style="text-align: center;">25</td>
      <td style="text-align: center;">5.6%</td>
    </tr>
    <tr>
      <th>PARTLY_RELEVANT</th>
      <td style="text-align: center;">38</td>
      <td style="text-align: center;">8.4%</td>
    </tr>
    <tr>
      <th>RELEVANT</th>
      <td style="text-align: center;">87</td>
      <td style="text-align: center;">19.3%</td>
    </tr>
    <tr>
      <th rowspan="4" valign="top">promt_template_3</th>
      <th>IMPORTANT_RELEVANT</th>
      <td style="text-align: center;">1</td>
      <td style="text-align: center;">0.2%</td>
    </tr>
    <tr>
      <th>NON_RELEVANT</th>
      <td style="text-align: center;">11</td>
      <td style="text-align: center;">2.4%</td>
    </tr>
    <tr>
      <th>PARTLY_RELEVANT</th>
      <td style="text-align: center;">54</td>
      <td style="text-align: center;">12.0%</td>
    </tr>
    <tr>
      <th>RELEVANT</th>
      <td style="text-align: center;">84</td>
      <td style="text-align: center;">18.7%</td>
    </tr>
  </tbody>
</table>
</div>


The best result is provided by simple prompt, so I used it in the application.