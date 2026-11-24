.PHONY: test reproduce reproduce-small app

test:
    python -m pytest --cov=scripts --cov-report=term-missing

reproduce-small:
    python -m scripts.executer_experiences --small

reproduce:
    python -m scripts.executer_experiences

app:
    python -m streamlit run app.py
