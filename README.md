Press CTRL + SHIFT + V if viewing this file in vscode

```bash
python -m venv env
```

```bash
.\env\Scripts\activate
```

```bash
pip install -r requirements.txt
```

Note: If the install is taking a long time, install the libraries from requirements.txt one by one

## Setting up env file

- Create a file called ".env"
- Add the following in it:

```plaintext
OPENAI_API_KEY=[Your Key]
```

## Setting up data
- add your docx files in the "data" subfolder

## Running the application
```bash
streamlit run frontend.py
```