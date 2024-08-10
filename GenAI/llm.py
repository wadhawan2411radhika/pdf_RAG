from llamaclient import LlamaClient
import yaml
import json

def swot_analysis(client, year):
    with open('query.yaml', 'r') as file:
            config = yaml.safe_load(file)

    swot_dict = {
        'strength': [f'results/strength_results_{year}.json', 
                     config['strength_prompt']],
        'weakness': [f'results/weakness_results_{year}.json', 
                     config['weakness_prompt']],
        'opportunity': [f'results/opportunity_results_{year}.json', 
                     config['opportunity_prompt']],
        'threat': [f'results/threat_results_{year}.json', 
                     config['threat_prompt']]
    }

    response = {}

    for key, value in swot_dict.items():
        with open(value[0], 'r') as file:
            context_data = json.load(file)
        context = " ".join(context_data)  # Modify this depending on how your JSON is structured
        prompt = value[1].format(context=context)
        response[key] = client.generate_analysis(prompt)
    
    prompt = config['summary_prompt'].format(
        strength=response['strength'],
        weakness=response['weakness'],
        opportunity=response['opportunity'],
        threat=response['threat']
    )
    return client.generate_analysis(prompt)


def main():
    # Initialize the Groq client
    groq_client = LlamaClient()
    analysis_22 = swot_analysis(groq_client, 2022)
    analysis_23 = swot_analysis(groq_client, 2023)

if __name__ == "__main__":
    main()