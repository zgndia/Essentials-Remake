__version__ = "1.0.0"

# Decrypting
# -------------------------
import requests
from cryptography.fernet import Fernet

GITHUB_TOKEN = "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"
GIST_ID = 'a24741cd53d2afdc453ba4aed06d9498'
FILENAME = 'Key.txt'

def get_gist_content():
    """Retrieve content from a GitHub Gist."""
    headers = {'Authorization': f'token {GITHUB_TOKEN}'}
    response = requests.get(f'https://api.github.com/gists/{GIST_ID}', headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        files = data.get('files', {})
        if FILENAME in files:
            return files[FILENAME]['content']
        else:
            print(f"File '{FILENAME}' not found in the Gist. Creating a new Gist.")
            return None
    else:
        print(f"Failed to get Gist content. Status Code: {response.status_code}")
        print(f"Response: {response.text}")
    return None

def update_gist_content(content):
    """Update the Gist with new content."""
    headers = {'Authorization': f'token {GITHUB_TOKEN}'}
    data = {'files': {FILENAME: {'content': content}}}
    response = requests.patch(f'https://api.github.com/gists/{GIST_ID}', json=data, headers=headers)
    
    if response.status_code == 200:
        print("Gist updated successfully.")
    else:
        print(f"Failed to update the Gist. Status Code: {response.status_code}")
        print(f"Response: {response.text}")

def create_gist(content):
    """Create a new Gist with the given content."""
    headers = {'Authorization': f'token {GITHUB_TOKEN}'}
    data = {
        'description': 'Key storage for encryption',
        'public': False,
        'files': {FILENAME: {'content': content}}
    }
    response = requests.post('https://api.github.com/gists', json=data, headers=headers)
    
    if response.status_code == 201:
        print("Gist created successfully.")
        return response.json()['id']
    else:
        print(f"Failed to create the Gist. Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        return None

def is_valid_fernet_key(key):
    """Check if the key is a valid Fernet key."""
    try:
        Fernet(key.encode())  # Try to initialize Fernet with the key
        return True
    except Exception:
        return False

def getKey():
    """Get the encryption key from the Gist or generate a new one if needed."""
    key = get_gist_content()
    if key is None or not is_valid_fernet_key(key.strip()):
        key = Fernet.generate_key().decode()
        new_gist_id = create_gist(key)
        if new_gist_id:
            global GIST_ID
            GIST_ID = new_gist_id
        else:
            update_gist_content(key)
    else:
        key = key.strip()  # Clean up any extraneous whitespace

    try:
        return Fernet(key.encode())  # Ensure key is properly formatted
    except Exception as e:
        print(f"Error initializing Fernet with key: {e}")
        raise
# -------------------------

# Essentials API

def roundify(n):
    import math
    m = 1
    return int(math.ceil(n*m)/m)

class string():
    
    def before(text: str, kw: str):
        return text[:text.index(kw)]

    def after(text: str, kw: str):
        return text[text.index(kw):].replace(kw,"")

class file():

    def read(file: str):
        try:
            with open(file, "r") as f:
                x = ''.join(f.readlines())
                if x == "":
                    return None
                return x
        except:
            return None
    
    def readlines(file: str):
        try:
            with open(file, "r") as f:
                x = f.readlines()
                if x == "[]":
                    return None
                return x

        except:
            return None
    
    def write(file: str, object: str):
        try:
            with open(file, "w") as f:
                f.write(object)
                return True
        except:
            return False
    
    def append(file: str, object: str):
        try:
            with open(file, "a") as f:
                f.write(object)
                return True

        except:
            return None
        
    def look_for(file: str, object: str):
        try:
            with open(file, "r") as f:
                list = f.readlines()
                l_en = []
                for x in list:
                    l_en.append(x.replace("\n",""))
                
                if object in l_en:
                    return True
                else:
                    return False
                
        except:
            return None

class text():

    def default(text: str):
        return text.capitalize().rstrip()
    
    def title(text: str):

        t: str= ""
        i = 0

        for x in text.split():
            if i == len(text.split()) - 1:
                t += x.capitalize()
            else:
                t += x.capitalize() + " "

            i += 1
        
        return t.rstrip()

class templates():

    def discord_py():

        template = ''.join(file.read("data\\dpy.txt"))

        if file.read("discord.py") == None:
            file.write("discord.py", template)
        else:
            loop = True
            i = 2
            while loop:
                if file.read("discord{}.py".format(i)) == None:
                    file.write("discord{}.py".format(i), template)
                    loop = False
                
                i += 1

class Decryption():

    def encode(message):
        """Encode a message using the encryption key."""
        fernet = getKey()
        return fernet.encrypt(message.encode()).decode()  # Encode to string for better readability

    def decode(encrypted_message):
        """Decode a message using the encryption key."""
        message = encrypted_message.encode()  # Convert to bytes for decryption
        fernet = getKey()
        return fernet.decrypt(message).decode()

    # Example usage
    #encode(msg), decode(msg)