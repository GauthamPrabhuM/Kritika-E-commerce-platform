# About The Project

A website to sell and purchase women's handicraft products. This was our submission for our Internet Technologies Lab miniproject. This project uses flask with sqlite3

# How to Use

## Creating A Virtual Environment

## Running The Server
## Kritika — E‑commerce platform (Flask)

Kritika is a simple Flask-based e‑commerce web app for selling and purchasing women's handicraft products. It was originally created as an Internet Technologies Lab miniproject and uses SQLite for storage.

### Highlights

- Flask + SQLite minimal web app
- Includes product pages, cart, user registration/login, and profile editing
- Static assets and product images included under `static/` and `uploads/`

## Quick start

Prerequisites: Python 3.8+ (system `python3`), and optionally `virtualenv`.

1. Create and activate a virtual environment

```bash
# from the project root
python3 -m venv venv
source venv/bin/activate
```

2. Install requirements

```bash
pip install -r requirements.txt
```

3. Run the app

```bash
python3 main.py
```

Open http://127.0.0.1:5000 in your browser.

Notes
- The project was developed against Flask 2.2.x; if you encounter compatibility issues, try installing the version pinned in `requirements.txt`.

## Development checklist

- Inspect or reset `database.db` if you want a fresh state
- Static assets live in `static/` and uploads in `uploads/`

## License

This project includes a `LICENSE` file in the repository. Check it for full terms.

## Acknowledgements

- Original authors and contributors of the Kritika miniproject.
- This README was reframed with assistance from a generative AI to improve clarity and structure; any editorial changes were reviewed and approved by the repository owner.

---

If you'd like, I can also create a small CONTRIBUTING section, add badges, or split setup steps into a `Makefile` or `scripts/` directory.

**Note: Replace python3 with python or py on Window installations**

**Note: VSCode terminal can autodetect virtual environments if they are named venv. Thus activating virtual environment is optional for VSCode users.**

```bash
# Note all commands are typed in the outer kritika folder
# Create a virtual environment named virtual
python3 -m venv virtual
# Activate the virtual environment
source ./virtual/bin/activate
# Install the requirements
pip install -r requirements.txt
```

## Running The Server

```bash
# Note all commands are typed in the outer kritika folder
# Start the server
python3 main.py
```

The server is now running. You can view it on a browser by visiting
http://127.0.0.1:5000