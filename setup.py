from setuptools import setup, find_packages

setup(
    name="chatgpt-agent-o3",
    version="1.0.0",
    description="ChatGPT Agent implementation following o3 research synthesis",
    author="O3 Research Team",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "fastapi>=0.104.0",
        "pydantic>=2.5.0",
        "redis>=5.0.0",
        "celery>=5.3.0",
        "prometheus-client>=0.19.0",
        "opentelemetry-api>=1.21.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-asyncio>=0.21.0",
            "pytest-cov>=4.1.0",
            "black>=23.0.0",
            "mypy>=1.7.0",
            "ruff>=0.1.0",
        ]
    },
    python_requires=">=3.11",
) 