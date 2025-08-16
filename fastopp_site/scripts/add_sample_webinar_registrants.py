#!/usr/bin/env python3
"""
Script to add sample webinar registrants with photos for testing the photo upload functionality
"""

import asyncio
import uuid
import shutil
from pathlib import Path
from datetime import datetime, timezone
from db import AsyncSessionLocal
from models import WebinarRegistrants


async def add_sample_registrants():
    """Add sample webinar registrants to the database with photos"""
    
    sample_registrants = [
        {
            "name": "John Smith",
            "email": "john.smith@example.com",
            "company": "Tech Corp",
            "webinar_title": "Advanced FastAPI Development",
            "webinar_date": datetime(2024, 2, 15, 14, 0, tzinfo=timezone.utc),
            "status": "registered",
            "photo_filename": "john_smith.jpg",
            "notes": ("Interested in implementing authentication systems. "
                      "Has experience with Django and wants to migrate to FastAPI.")
        },
        {
            "name": "Sarah Johnson",
            "email": "sarah.johnson@startup.io",
            "company": "Startup Inc",
            "webinar_title": "Building Scalable APIs",
            "webinar_date": datetime(2024, 2, 20, 10, 0, tzinfo=timezone.utc),
            "status": "attended",
            "photo_filename": "sarah_johnson.jpg",
            "notes": ("Startup founder looking to scale their API from 100 to 10,000 users. "
                      "Currently using Express.js and considering FastAPI for better performance.")
        },
        {
            "name": "Michael Chen",
            "email": "michael.chen@enterprise.com",
            "company": "Enterprise Solutions",
            "webinar_title": "Database Design Best Practices",
            "webinar_date": datetime(2024, 2, 25, 16, 0, tzinfo=timezone.utc),
            "status": "registered",
            "photo_filename": "michael_chen.jpg",
            "notes": ("Senior architect evaluating database solutions for a new microservices project. "
                      "Interested in PostgreSQL and Redis integration patterns.")
        },
        {
            "name": "Emily Davis",
            "email": "emily.davis@freelance.dev",
            "company": "Freelance Developer",
            "webinar_title": "Modern Web Development",
            "webinar_date": datetime(2024, 3, 1, 13, 0, tzinfo=timezone.utc),
            "status": "registered",
            "photo_filename": "emily_davis.jpg",
            "notes": ("Full-stack developer specializing in React and Node.js. "
                      "Looking to expand skillset to include Python and FastAPI for backend development.")
        },
        {
            "name": "David Wilson",
            "email": "david.wilson@consulting.co",
            "company": "Tech Consulting",
            "webinar_title": "API Security Fundamentals",
            "webinar_date": datetime(2024, 3, 5, 15, 0, tzinfo=timezone.utc),
            "status": "registered",
            "photo_filename": "david_wilson.jpg",
            "notes": ("Security consultant working with financial services clients. "
                      "Needs to implement OAuth2 and JWT token validation for compliance requirements.")
        }
    ]
    
    # Setup photo directories
    sample_photos_dir = Path("static/uploads/sample_photos")
    photos_dir = Path("static/uploads/photos")
    photos_dir.mkdir(exist_ok=True)
    
    async with AsyncSessionLocal() as session:
        for registrant_data in sample_registrants:
            # Check if registrant already exists
            from sqlmodel import select
            existing = await session.execute(
                select(WebinarRegistrants).where(WebinarRegistrants.email == registrant_data['email'])
            )
            if existing.scalar_one_or_none():
                print(f"Registrant {registrant_data['email']} already exists, skipping...")
                continue
            
            # Copy sample photo if it exists
            photo_url = None
            photo_filename = registrant_data.pop('photo_filename')
            sample_photo_path = sample_photos_dir / photo_filename
            
            if sample_photo_path.exists():
                # Generate unique filename for the photo
                unique_filename = f"{uuid.uuid4()}_{photo_filename}"
                photo_dest_path = photos_dir / unique_filename
                
                # Copy the sample photo
                shutil.copy2(sample_photo_path, photo_dest_path)
                photo_url = f"/static/uploads/photos/{unique_filename}"
                print(f"✓ Copied photo for {registrant_data['name']}")
            else:
                print(f"⚠ Sample photo not found: {photo_filename}")
            
            # Create new registrant
            registrant = WebinarRegistrants(
                id=uuid.uuid4(),
                name=registrant_data['name'],
                email=registrant_data['email'],
                company=registrant_data['company'],
                webinar_title=registrant_data['webinar_title'],
                webinar_date=registrant_data['webinar_date'],
                status=registrant_data['status'],
                notes=registrant_data['notes'],
                photo_url=photo_url
            )
            
            session.add(registrant)
            print(f"Added registrant: {registrant_data['name']} ({registrant_data['email']})")
        
        await session.commit()
        print(f"\nSuccessfully added {len(sample_registrants)} sample webinar registrants with photos!")


if __name__ == "__main__":
    asyncio.run(add_sample_registrants()) 