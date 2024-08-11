from llamaclient import LlamaClient
import yaml
import json

def swot_analysis(client, year):
    with open('query.yaml', 'r') as file:
            config = yaml.safe_load(file)

    swot_dict = {
        f'strength_{year}': [f'results/{year}_strength_results.json', 
                     config['strength_prompt']],
        f'weakness_{year}': [f'results/{year}_weakness_results.json', 
                     config['weakness_prompt']],
        f'opportunity_{year}': [f'results/{year}_opportunity_results.json', 
                     config['opportunity_prompt']],
        f'threat_{year}': [f'results/{year}_threat_results.json', 
                     config['threat_prompt']]
    }
    response = {}

    for key, value in swot_dict.items():
        with open(value[0], 'r') as file:
            context_data = json.load(file)
        context = " ".join(context_data)  # Modify this depending on how your JSON is structured
        prompt = value[1].format(context=context)
        response[key] = client.generate_analysis(prompt)
    return response

def summary_prompt(client, response):
    with open('query.yaml', 'r') as file:
        config = yaml.safe_load(file)

    prompt = config['summary_prompt'].format(
        strength_2022=response['strength_2022'],
        weakness_2022=response['weakness_2022'],
        opportunity_2022=response['opportunity_2022'],
        threat_2022=response['threat_2022'],
        strength_2023=response['strength_2023'],
        weakness_2023=response['weakness_2023'],
        opportunity_2023=response['opportunity_2023'],
        threat_2023=response['threat_2023'],
    )
    return client.generate_analysis(prompt)

def main():
    # Initialize the Groq client
    groq_client = LlamaClient()
    analysis_22 = swot_analysis(groq_client, 2022)
    analysis_23 = swot_analysis(groq_client, 2023)
    response = {**analysis_22, **analysis_23}
    response = summary_prompt(groq_client, response)
    print(response)
    with open('results/swot.md', 'w') as file:
        file.write(response)

if __name__ == "__main__":
    main()