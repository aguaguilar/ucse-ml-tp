import requests


def clean_dataframe(df):
	rename_columns = {
	    'age_A': 'edad_a', 'age_B': 'edad_b', 'height_A': 'altura_a', 
	    'height_B': 'altura_b', 'reach_A': 'alcance_mano_a',
	    'reach_B': 'alcance_mano_b', 'stance_A': 'posicion_a', 'stance_B': 'posicion_b',
	    'weight_A': 'peso_a', 'weight_B': 'peso_b', 'won_A': 'ganadas_a', 'won_B': 'ganadas_b',
	       'lost_A': 'perdidas_a', 'lost_B': 'perdidas_b', 'drawn_A': 'empatadas_a', 'drawn_B':'empatadas_b',
	    'kos_A': 'kos_a', 'kos_B': 'kos_b', 'result': 'resultado', 'decision': 'decision',
	    'judge1_A': 'juez1_a', 'judge1_B': 'juez1_b', 'judge2_A': 'juez2_a', 'judge2_B': 'juez2_b', 
	    'judge3_A': 'juez3_a', 'judge3_B': 'juez3_b'
	}
	df.rename(columns=rename_columns, inplace=True)
	df = df.drop(df[(df['edad_a'].isnull()) | (df['edad_b'].isnull())].index)
	df = df.drop(df[(df['edad_a'] <= 18) | (df['edad_b'] <= 18)].index)
	df = df.drop(df[(df['altura_a'] <= 100) | (df['altura_b'] <= 100)].index)
	df = df.drop(df[(df['altura_a'].isnull()) | (df['altura_b'].isnull())].index)
	df = df.drop(["alcance_mano_a", "alcance_mano_b"], axis=1)
	df = df.drop(["decision", "juez1_a", "juez1_b", "juez2_a", "juez2_b", "juez3_a", "juez3_b"], axis=1)
	df["gano"] = df.resultado == 'win_A'
	df = df.drop(["peso_a", "peso_b"], axis=1)

	return df


def download_file_from_google_drive(id, destination):
    URL = "https://docs.google.com/uc?export=download"

    session = requests.Session()

    response = session.get(URL, params = { 'id' : id }, stream = True)
    token = get_confirm_token(response)

    if token:
        params = { 'id' : id, 'confirm' : token }
        response = session.get(URL, params = params, stream = True)

    save_response_content(response, destination)    

def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value

    return None

def save_response_content(response, destination):
    CHUNK_SIZE = 32768

    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)