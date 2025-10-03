import ollama
import json

model_name = 'llama3.2'
prompt_file = 'sysprompt.txt'
system_prompt = None
customer_data_file = 'Customer.json'

# Definicion de funcion para actualizar el archivo de datos del cliente
def update_customer_data(new_data):
    with open(customer_data_file, 'a', encoding='utf-8') as f:
        f.write(new_data)

# Definicion de funcion para cargar datos del cliente
def load_customer_data(username, password):
    with open(customer_data_file, 'r', encoding='utf-8') as f:
        # Leer archivo json y buscar username y password
        data = json.load(f)
        for customer in data:
            if customer.get('user_name') == username and customer.get('password') == password:
                customer['password'] = '****'  # Ocultar la contraseña
                return customer
        # Si no se encuentra el usuario, retornar None
        return None
    
def load_system_prompt(prompt_file, current_customer):

    # abrir y leer el archivo de prompt y el archivo JSON
    with open(prompt_file, 'r', encoding='utf-8') as f:
        system_prompt = f.read()
    
    # Reemplaza el marcador de posición [JSON_FILE] con el contenido del archivo JSON
    system_prompt = system_prompt.replace("[CUSTOMER]", str(current_customer))
    return system_prompt


print("Bienvenido a 🐶 VeterinarIA 🤖\n Para comenzar inicie sesión con (I) o (X) para Salir)")

while(1):
    user_input = input("👨 PetLover: ")
    if user_input.lower() == "x":
        break
    elif user_input.lower() == "i":
        username = input("Ingrese su nombre de usuario: ")
        import getpass
        password = getpass.getpass('Ingrese su contraseña: ')
        customer = load_customer_data(username, password)
        print(str(customer))
        if customer is not None:
            current_customer = customer
            system_prompt = load_system_prompt(prompt_file, current_customer)
            print(f"Bienvenido a 🐶🤖 VeterinarIA  {customer.get('nombre_usuario')}!")
            print(f"¿Cómo podemos ayudarle?. ¿Su {json.dumps(customer["mascota"]['nombre'])} se encuentra bien?")
        else:
            print("Nombre de usuario o contraseña incorrectos. Intente de nuevo.")
            continue
    else:
        response = ollama.chat(
        model=model_name,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
            ]
        )
        response_content = response['message']['content']
        if "UPDATE_RECORD" in response_content:
            # Extraer el JSON de la respuesta
            start_index = response_content.index("UPDATE_RECORD") + len("UPDATE_RECORD")
            json_data = response_content[start_index:].strip()
            update_customer_data(json_data)
            print("Registro de cliente actualizado.")
        print("🐶🤖 VeterinarIA:", response['message']['content'])