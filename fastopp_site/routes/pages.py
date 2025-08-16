"""
Page routes for rendering HTML templates
"""
from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from auth.core import get_current_staff_or_admin_from_cookies
from models import User

templates = Jinja2Templates(directory="templates")

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Home page"""
    return templates.TemplateResponse("index.html", {
        "request": request, 
        "title": "FastOpp - Easier AI Web Apps",
        "current_page": "home"
    })


@router.get("/volunteers", response_class=HTMLResponse)
async def volunteers(request: Request):
    """Volunteers page"""
    return templates.TemplateResponse("volunteers.html", {
        "request": request,
        "title": "Call For Volunteers - FastOpp",
        "current_page": "volunteers"
    })


@router.get("/project", response_class=HTMLResponse)
async def project(request: Request):
    """Project page"""
    return templates.TemplateResponse("project.html", {
        "request": request,
        "title": "Project Description - FastOpp",
        "current_page": "project"
    })


@router.get("/docs", response_class=HTMLResponse)
async def docs(request: Request):
    """Documentation page"""
    return templates.TemplateResponse("docs.html", {
        "request": request,
        "title": "Documentation - FastOpp",
        "current_page": "docs"
    })


@router.get("/documentation", response_class=HTMLResponse)
async def documentation(request: Request):
    """Documentation page"""
    return templates.TemplateResponse("docs.html", {
        "request": request,
        "title": "Documentation - FastOpp",
        "current_page": "documentation"
    })


@router.get("/tutorials", response_class=HTMLResponse)
async def tutorials(request: Request):
    """Tutorials page"""
    return templates.TemplateResponse("tutorials.html", {
        "request": request,
        "title": "Tutorials - FastOpp",
        "current_page": "tutorials"
    })


@router.get("/design-demo", response_class=HTMLResponse)
async def design_demo(request: Request):
    """Design demo page"""
    return templates.TemplateResponse("design-demo.html", {"request": request, "title": "FastOpp Design Demo"})


@router.get("/dashboard-demo", response_class=HTMLResponse)
async def dashboard_demo(request: Request):
    """Product dashboard demo page"""
    return templates.TemplateResponse("dashboard-demo.html", {"request": request, "title": "Product Dashboard Demo"})


@router.get("/webinar-registrants", response_class=HTMLResponse)
async def webinar_registrants(request: Request, current_user: User = Depends(get_current_staff_or_admin_from_cookies)):
    """Webinar registrants management page"""
    return templates.TemplateResponse("webinar-registrants.html", {
        "request": request, 
        "title": "Webinar Registrants",
        "current_page": "webinar-registrants"
    })


@router.get("/webinar-demo", response_class=HTMLResponse)
async def webinar_demo(request: Request):
    """Marketing page showcasing webinar attendees and community"""
    return templates.TemplateResponse("webinar-demo.html", {
        "request": request, 
        "title": "Webinar Demo",
        "current_page": "webinar-demo"
    })


@router.get("/ai-demo", response_class=HTMLResponse)
async def ai_demo(request: Request):
    """AI Chat demo page with Llama 3.3 70B integration"""
    return templates.TemplateResponse("ai-demo.html", {
        "request": request,
        "title": "AI Chat Demo",
        "current_page": "ai-demo"
    })


@router.get("/ai-stats", response_class=HTMLResponse)
async def ai_stats(request: Request):
    """HTMX endpoint to return AI marketing statistics"""
    import time
    time.sleep(1)  # Simulate processing time

    stats = [
        {"metric": "Content Generation Speed", "value": "10x Faster", "icon": "⚡"},
        {"metric": "Campaign ROI", "value": "+340%", "icon": "📈"},
        {"metric": "Time Saved", "value": "87%", "icon": "⏰"},
        {"metric": "Engagement Rate", "value": "+280%", "icon": "🎯"}
    ]

    return templates.TemplateResponse("partials/ai-stats.html", {
        "request": request,
        "stats": stats
    })


@router.post("/marketing-demo", response_class=HTMLResponse)
async def marketing_demo(request: Request):
    """HTMX endpoint to handle marketing demo form submission"""
    # In a real app, you'd parse form data properly
    # For demo purposes, we'll simulate form processing
    import time
    time.sleep(1.5)  # Simulate processing time

    return templates.TemplateResponse("partials/demo-response.html", {
        "request": request,
        "success": True,
        "message": "Thank you! Our AI team will contact you within 24 hours with a personalized marketing demo."
    })


@router.get("/license")
async def license_page(request: Request):
    """License page"""
    return templates.TemplateResponse("license.html", {
        "request": request,
        "title": "MIT License"
    }) 