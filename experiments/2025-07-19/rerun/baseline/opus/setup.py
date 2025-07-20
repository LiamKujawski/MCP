from setuptools import setup, find_packages

setup(
    name="chatgpt-agent-opus",
    version="1.0.0",
    description="ChatGPT Agent implementation following Claude-4-Opus unified approach",
    author="Claude-4-Opus Research Team",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "fastapi>=0.104.0",
        "pydantic>=2.5.0",
        "redis>=5.0.0",
        "celery>=5.3.0",
        "prometheus-client>=0.19.0",
        "opentelemetry-api>=1.21.0",
        "aiofiles>=23.2.0",
        "python-multipart>=0.0.6",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-asyncio>=0.21.0",
            "pytest-cov>=4.1.0",
            "black>=23.0.0",
            "mypy>=1.7.0",
            "ruff>=0.1.0",
            "httpx>=0.25.0",
        ]
    },
    python_requires=">=3.11",
) 