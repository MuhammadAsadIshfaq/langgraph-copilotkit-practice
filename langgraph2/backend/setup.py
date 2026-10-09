from setuptools import setup, find_packages

setup(
    name="hiring-workflow",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn",
        "langgraph",
        "groq",
        "langchain",
        "langchain-core",
        "langchain-groq",
        "PyPDF2",
        "python-docx",
        "mammoth",
        "email-validator",
        "python-multipart",
        "pydantic"
    ],
) 