import boto3, json
import streamlit as st

ANTHROPIC_OUTPUT = 'output = response_body[\'completion\']'
COHERE_OUTPUT = 'output = response_body[\'generations\'][0][\'text\'] '
A121_OUTPUT = 'output = response_body.get("completions")[0].get("data").get("text")'
BEDROCK_RUNTIME = 'bedrock_runtime = boto3.client( service_name=\'bedrock-runtime\',region_name="us-east-1")\n'
MODEL_CODE_IMPORT='import boto3, json \n\n'
REQUEST_BODY= 'response = bedrock_runtime.invoke_model(body=body, modelId=modelId, accept=\'application/json\', contentType=\'application/json\')\n'
MODEL_CODE_RESPONSE_BODY = 'response_body = json.loads(response.get(\'body\').read())\n'
PRINT_OUTPUT = 'print ("Output = )'

gen_ai_models = ['AI21 Labs : ai21.j2-grande-instruct',
                 'AI21 Labs : ai21.j2-jumbo-instruct',
                 'AI21 Labs : ai21.j2-mid',
                 'AI21 Labs : ai21.j2-mid-v1',
                 'AI21 Labs : ai21.j2-ultra',
                 'AI21 Labs : ai21.j2-ultra-v1',
                 'Anthropic : anthropic.claude-instant-v1',
                 'Anthropic : anthropic.claude-v1',
                 'Anthropic : anthropic.claude-v2',
                 'Cohere : cohere.command-text-v14']

model_parameters = {
    "Anthropic": {
        "prompt": '',
        "max_tokens_to_sample": '',
        "temperature": '',
        "top_p": '',
    },
    "AI21Labs": {
        "prompt": '',
        "maxTokens": '',
        "temperature": '',
        "topP": '',
    },
    "Amazon": {
        "prompt": '',
        "maxTokens": '',
        "temperature": '',
        "topP": '',
    },
    "Cohere": {
        "prompt": '',
        "max_tokens": '',
    },
}


# Initialize Streamlit layout
st.title("AWS Bedrock")
# Run the Bedrock model
bedrock_runtime = boto3.client(
    service_name='bedrock-runtime',
    region_name="us-east-1"
)

# Generate the parameters based on the 
def generate_python_code(model_vendor, modelId, body, output):
    st.write("Python Code")
    if (model_vendor == 'Anthropic'):
        MODEL_RESPONSE_OUTPUT = ANTHROPIC_OUTPUT
    elif (model_vendor == 'Cohere'):   
        MODEL_RESPONSE_OUTPUT = COHERE_OUTPUT 
    elif (model_vendor == 'AI21Labs'):
        MODEL_RESPONSE_OUTPUT = A121_OUTPUT                          
    MODEL_CODE = MODEL_CODE_IMPORT + \
        BEDROCK_RUNTIME + \
        'body = json.dumps(' + body  + ')' + '\n'+ \
        'modelId = ' + '"' + modelId + '"' + '\n' + \
        REQUEST_BODY + \
        MODEL_CODE_RESPONSE_BODY + \
        MODEL_RESPONSE_OUTPUT + '\n' + \
        'print (output)'
     
    return MODEL_CODE

with st.container():
    genai_model_id = st.selectbox("Generative AI model",
        (sorted(gen_ai_models)),
        index=None,
        placeholder="Select Generative Model..",
        )

    if (genai_model_id != None):
        model_vendor = str(genai_model_id.split(':')[0]).replace(" ", "")

        # Generate the model invocation
        #prompt = st.text_area("Prompt...")
        for key in model_parameters[model_vendor]:
            print("*****KEY*******", key)
            if (key == 'prompt'):
                value = st.text_area("Prompt...")
                if (model_vendor == "Anthropic"):
                    value = "Human: " + value + "\n\n Assistant:"
                print ("11.***********", value)
            if (key == "max_tokens_to_sample") or (key =="maxTokens") or (key == "max_tokens"):
                 value = st.slider("Number of Max Tokens",  1, 8000)
            if (key == "temperature"):
                value = st.slider("Temperature",  0.0, 1.0, step=0.1)
            if (key == "top_p") or (key == "topP"):
                value = st.slider("topP",  0.0, 1.0, step=0.1)   
            model_parameters[model_vendor][key] = value           
        body = json.dumps(model_parameters[model_vendor])
        modelId = str(genai_model_id.split(':')[1]).replace(" ", "")

        # Invoke the Bedrock runtime
        generate = st.button("Generate")
        if (generate):
            try:
                response = bedrock_runtime.invoke_model(body=body, modelId=modelId, accept='application/json', contentType='application/json')
                response_body = json.loads(response.get('body').read())
                if (model_vendor == "Anthropic"):
                    output = response_body['completion']
                elif (model_vendor == "Cohere"):
                    output = response_body['generations'][0]['text'] 
                else:    
                    output = response_body.get("completions")[0].get("data").get("text")
                st.text_area("Response ...", value=output)

                model_code = generate_python_code(model_vendor, modelId, body, output)
                st.code(model_code, language='python')
            except Exception as e:
                st.error(e)
                

