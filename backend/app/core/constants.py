UPLOAD_DIRECTORY = "storage/repositories_collections"

EXTENSION_LANGUAGE_MAP = {
    ".py": "Python",
    ".js": "JavaScript",
    ".ts": "TypeScript",
    ".jsx": "React",
    ".tsx": "React",
    ".java": "Java",
    ".kt": "Kotlin",
    ".php": "PHP",
    ".go": "Go",
    ".cs": "C#",
    ".cpp": "C++",
    ".c": "C",
    ".rs": "Rust",
    ".swift": "Swift",
    ".rb": "Ruby",
    ".html": "HTML",
    ".css": "CSS",
    ".scss": "SCSS",
    ".json": "JSON",
    ".xml": "XML",
    ".sql": "SQL",
    ".md": "Markdown",
    ".sh": "Shell"
}

FRAMEWORK_PATTERNS = {
    "requirements.txt": {
        "fastapi": "FastAPI",
        "django": "Django",
        "flask": "Flask"
    },

    "package.json": {
        "\"react\"": "React",
        "\"next\"": "Next.js",
        "\"express\"": "Express",
        "\"nestjs\"": "NestJS"
    },

    "composer.json": {
        "laravel/framework": "Laravel"
    },

    "pom.xml": {
        "spring-boot": "Spring Boot"
    }
}

LIBRARY_PATTERNS = {

    "requirements.txt": {
        "sqlalchemy": "SQLAlchemy",
        "pydantic": "Pydantic",
        "redis": "Redis",
        "celery": "Celery",
        "numpy": "NumPy",
        "pandas": "Pandas",
        "tensorflow": "TensorFlow",
        "scikit-learn": "Scikit-learn",
        "opencv-python": "OpenCV",
        "pytest": "Pytest"
    },

    "package.json": {
        "\"axios\"": "Axios",
        "\"redux\"": "Redux",
        "\"mongoose\"": "Mongoose",
        "\"socket.io\"": "Socket.IO",
        "\"tailwindcss\"": "Tailwind CSS",
        "\"typeorm\"": "TypeORM",
        "\"prisma\"": "Prisma"
    }
}