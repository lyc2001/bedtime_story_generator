from flask_ngrok import run_with_ngrok
from flask import Flask, render_template, request

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import transformers
import torch
import base64
from io import BytesIO



model = "tom92119/llama-2-7b-bedtime-story"
tokenizer = AutoTokenizer.from_pretrained(model)

falcon_pipeline = transformers.pipeline("text-generation",
                                        model=model,
                                        tokenizer=tokenizer,
                                        torch_dtype=torch.bfloat16,
                                        trust_remote_code=True,
                                        device_map=0
                                        )


# define completion function
def get_completion_falcon(input):
  prompt = f"<s>[INST] {input} [/INST]"
  #print(prompt)
  falcon_response = falcon_pipeline(prompt,
                                    max_length=300,
                                    do_sample=True,
                                    top_k=10,
                                    num_return_sequences=1,
                                    eos_token_id=tokenizer.eos_token_id,
                                    )

  return falcon_response

# Start flask app and set to ngrok
app = Flask(__name__)
run_with_ngrok(app)

@app.route('/')
def initial():
  return render_template('index.html')

@app.route('/submit-prompt', methods=['POST'])
def generate_text():
    prompt = request.form['prompt-input']
    print(f"Generating text for prompt: {prompt}")

    # Call the text generation function
    response = get_completion_falcon(prompt)
    generated_text = response[0]['generated_text']
    parts = generated_text.split('[/INST]')
    generated_text = parts[1].strip()
  
    print("Text generated!")

    print("Sending text ...")
    return render_template('index.html', generated_text=generated_text)




if __name__ == '__main__':
    app.run()
