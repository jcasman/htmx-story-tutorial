# FastOpp Marketing Site

A modern marketing website for FastOpp, built with the same technology stack as the main FastOpp framework.

## About FastOpp

FastOpp is a FastAPI starter package for AI web applications. It uses pre-built admin components to give FastAPI functionality comparable to Django for AI-first applications.

## Features

- **Modern Design**: Built with Tailwind CSS, Alpine.js, and HTMX
- **Responsive Layout**: Mobile-first design that works on all devices
- **Fast Performance**: Static site generation with FastAPI
- **SEO Optimized**: Clean URLs and semantic HTML structure

## Technology Stack

- **Backend**: FastAPI
- **Templates**: Jinja2
- **Styling**: Tailwind CSS
- **Interactivity**: Alpine.js
- **Package Manager**: uv

## Getting Started

### Prerequisites

- Python 3.12+
- uv package manager

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd fastopp_site
```

2. Install dependencies:
```bash
uv sync
```

3. Initialize the site:
```bash
uv run python oppman.py init
```

4. Run the development server:
```bash
uv run python oppman.py runserver
```

5. Open your browser and visit `http://localhost:8000`

## Project Structure

```
fastopp_site/
├── main.py                 # FastAPI application
├── templates/              # Jinja2 templates
│   ├── index.html         # Homepage
│   ├── volunteers.html    # Volunteers page
│   ├── project.html       # Project description
│   ├── docs.html          # Documentation links
│   ├── tutorials.html     # Tutorials page
│   └── partials/          # Template partials
│       ├── header.html    # Navigation header
│       └── footer.html    # Site footer
├── static/                # Static assets
│   ├── css/              # Stylesheets
│   ├── js/               # JavaScript files
│   └── images/           # Image files
├── docs/                 # Additional documentation
├── pyproject.toml        # Project dependencies
└── README.md            # This file
```

## Pages

- **Homepage** (`/`): Main landing page with overview and features
- **Volunteers** (`/volunteers`): Call for volunteers information
- **Project** (`/project`): Detailed project architecture and benefits
- **Documentation** (`/documentation`): Links to FastOpp documentation
- **Tutorials** (`/tutorials`): Links to FastOpp tutorials

## Deployment

This site can be deployed to any platform that supports FastAPI applications:

- **Fly.io**: Use the same deployment process as the main FastOpp application
- **Railway**: Simple deployment with automatic scaling
- **Render**: Free tier available for static sites
- **Vercel**: Serverless deployment with edge functions

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test locally
5. Submit a pull request

## License

This project is licensed under the same MIT License as the main FastOpp repository.

## Links

- [FastOpp Repository](https://github.com/Oppkey/fastopp)