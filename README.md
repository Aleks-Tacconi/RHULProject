## Info
- Docstring conventions: [Google Style Docstrings](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html)
- Python version - 3.13.1

## How to run
1. Clone the repository:

    ```sh
    git clone git@github.com:Aleks-Tacconi/RHULProject.git
    ```

2. Navigate to the repository:
    
    ```sh
    cd RHULProject
    ```

3. Create and source a virtual environment:

    ```sh
    python -m venv venv
    source venv/bin/activate # On Linux/MacOS
    .\venv\Scripts\activate  # On Windows
    ```

4. Export OPENAI_API_KEY:

    ```sh
    export OPENAI_API_KEY="your_api_key" # On Linux/MacOS
    $env:OPENAI_API_KEY="your_api_key"   # On Windows
    ```

5. Run the program:

    ```sh
    python main.py
    ```
