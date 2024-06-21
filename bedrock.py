import boto3, json
import streamlit as st    

model_parameters = []

ANTHROPIC_PROMPT_PREFIX="Human:"
ANTHROPIC_PROMPT_SUFFIX="Assistant:"

#initialize streamlit layout
st.title("AWS Bedrock")

#list all the generative AI models supported in Bedrock
bedrock = boto3.client(service_name='bedrock')

model_type_id = [] 
for model_type in bedrock.list_foundation_models()['modelSummaries']:
    model_id = model_type['providerName'] + " : " + model_type['modelId']
    model_type_id.append(model_id)


# Run the Bedrock model 
bedrock_runtime = boto3.client(
    service_name='bedrock-runtime',
    region_name="us-east-1"
    )

with st.container():
    genai_model_id = st.selectbox("Generative AI model",
        (set(model_type_id)),
        index=None,
        placeholder="Select Generative Model..",
        )
    
    if (genai_model_id != None):
        print(" GEN AI model ID:   ", genai_model_id)
        model_vendor = str(genai_model_id.split(':')[0]).replace(" ", "")
        print ("model_vendor:  ", model_vendor)
        #modelId = genai_model_id.split(':')[1].lstrip()
        modelId = str(genai_model_id.split(':')[1]).replace(" ", "")
        print ("modeId:  ", modelId)
        

    #Amazon and A121 models
    #AI21 Labs : ai21.j2-ultra-v1
    #AI21 Labs : ai21.j2-jumbo-instruct
    #AI21 Labs : ai21.j2-grande-instruct
    #AI21 Labs : ai21.j2-ultra
    if (model_vendor == 'AI21Labs') or (model_vendor == 'Amazon'):
        print ("In if statement:  ", model_vendor)

        maxTokens = st.slider("Number of Max Tokens",  1, 8000)
        temperature = st.slider("Temperature",  0.0, 1.0, step=0.1)
        maxTokens = st.slider("topP",  0.0, 1.0, step=0.1)

        #build the prompt
        prompt = st.text_area("Prompt...")
        body = json.dumps({"prompt": prompt,
                            "maxTokens": 200,
                            "temperature": 0.5,
                            "topP": 0.5})
        accept = 'application/json'
        contentType = 'application/json'
        api = st.text_area("Bedrock Client invokation",
                            "body : " + body + '\n' + 
                            "modeld : " + model_id + '\n' + 
                            "contentType : " + contentType + '\n' + 
                            "accept : " + accept)
        generate = st.button("Generate")
        if (generate):
            response = bedrock_runtime.invoke_model(body=body, modelId=modelId, accept=accept, contentType=contentType)
            response_body = json.loads(response.get('body').read())
            output = response_body.get("completions")[0].get("data").get("text")
            res = st.text_area("Response ...", value = output)

        print ("_____________________________________________________________________")
        print ("_____________________________________________________________________")
        print ("Body:  ", body)
        print ("modelId:  ", modelId)
        print ("contentType:  ", contentType)
        print ("accept:  ", accept)
        print ("_____________________________________________________________________")
        print ("_____________________________________________________________________")


    #Anthropic model
    #anthropic.claude-v2
    #anthropic.claude-instant-v1
    if (model_vendor == 'Anthropic'):
        maxTokens = st.slider("Maximum tokens to sample",  1, 8000)
        temperature = st.slider("Temperature",  0.0, 1.0, step=0.1)
        top_p = st.slider("top_p",  0.0, 1.0, step=0.1)

        prompt = st.text_area("Prompt...")
        prompt = "Human: " + prompt + " Assistant:"

        body = json.dumps({
            "prompt": prompt,  
            "max_tokens_to_sample": maxTokens,
            "temperature": temperature,
            "top_p": top_p,
            })
        accept = 'application/json'
        contentType = 'application/json'
        response =  bedrock_runtime.invoke_model(body=body, modelId=modelId, accept=accept, contentType=contentType)
        response_body = json.loads(response.get('body').read())
        res = st.text_area("Response ...", value = response_body['completion'])

        print ("_____________________________________________________________________")
        print ("_____________________________________________________________________")
        print (" Type response: ", type(response_body))
        print ("Body:  ", body)
        print ("modelId:  ", modelId)
        print ("contentType:  ", contentType)
        print ("accept:  ", accept)
        print ("_____________________________________________________________________")
        print ("_____________________________________________________________________")


    #Cohere
    if (model_vendor == 'Cohere'):
        maxTokens = st.slider("Maximum tokens to sample",  1, 8000)
        prompt = st.text_area("Prompt...")
        body = json.dumps({
            "prompt": prompt,  
            "max_tokens": maxTokens,
            })
        accept = 'application/json'
        contentType = 'application/json'
      
        generate = st.button("Generate")
        if (generate):
            response =  bedrock_runtime.invoke_model(body=body, modelId=modelId, accept=accept, contentType=contentType)
            response_body = json.loads(response.get('body').read())
            res = st.text_area("Response ...", value = response_body['generations'][0]['text'])
        print ("_____________________________________________________________________")
        print ("_____________________________________________________________________")
        #print (" Type response: ", (response_body))
        print ("Body:  ", body)
        print ("modelId:  ", modelId)
        print ("contentType:  ", contentType)
        print ("accept:  ", accept)
        print ("_____________________________________________________________________")
        print ("_____________________________________________________________________")
        
        




 



