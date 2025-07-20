from setuptools import setup, find_packages

setup(
    name="chatgpt-agent-sonnet",
    version="1.0.0",
    description="ChatGPT Agent implementation following Claude-4-Sonnet holistic approach",
    author="Claude-4-Sonnet Research Team",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "fastapi>=0.104.0",
        "pydantic>=2.5.0",
        "redis>=5.0.0",
        "celery>=5.3.0",
        "prometheus-client>=0.19.0",
        "opentelemetry-api>=1.21.0",
        "sqlalchemy>=2.0.0",
        "alembic>=1.13.0",
        "structlog>=23.2.0",
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
    entry_points={
        "console_scripts": [
            "agent-server=src.main:main",
        ],
    },
) 