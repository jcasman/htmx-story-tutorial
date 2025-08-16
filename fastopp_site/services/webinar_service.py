"""
Webinar service for handling webinar registrant business logic
"""
from pathlib import Path
from typing import Optional
from uuid import UUID
import uuid
from sqlmodel import select
from db import AsyncSessionLocal
from models import WebinarRegistrants


class WebinarService:
    """Service for webinar registrant operations"""
    
    @staticmethod
    async def get_all_registrants():
        """Get all webinar registrants with their photos"""
        async with AsyncSessionLocal() as session:
            result = await session.execute(select(WebinarRegistrants))
            registrants = result.scalars().all()
            
            return [
                {
                    "id": str(registrant.id),
                    "name": registrant.name,
                    "email": registrant.email,
                    "company": registrant.company,
                    "webinar_title": registrant.webinar_title,
                    "webinar_date": registrant.webinar_date.isoformat(),
                    "status": registrant.status,
                    "photo_url": registrant.photo_url,
                    "notes": registrant.notes,
                    "registration_date": registrant.registration_date.isoformat()
                }
                for registrant in registrants
            ]
    
    @staticmethod
    async def get_webinar_attendees():
        """Get webinar attendees for the marketing demo page"""
        async with AsyncSessionLocal() as session:
            result = await session.execute(select(WebinarRegistrants))
            registrants = result.scalars().all()
            
            return [
                {
                    "id": str(registrant.id),
                    "name": registrant.name,
                    "email": registrant.email,
                    "company": registrant.company,
                    "webinar_title": registrant.webinar_title,
                    "webinar_date": registrant.webinar_date.isoformat(),
                    "status": registrant.status,
                    "group": registrant.group,
                    "notes": registrant.notes,
                    "photo_url": registrant.photo_url,
                    "created_at": registrant.created_at.isoformat()
                }
                for registrant in registrants
            ]
    
    @staticmethod
    async def upload_photo(registrant_id: str, photo_content: bytes, filename: str) -> tuple[bool, str, Optional[str]]:
        """
        Upload a photo for a webinar registrant
        
        Returns:
            tuple: (success, message, photo_url)
        """
        try:
            # Generate unique filename
            file_extension = Path(filename).suffix if filename else '.jpg'
            unique_filename = f"{uuid.uuid4()}{file_extension}"
            file_path = Path("static/uploads/photos") / unique_filename
            
            # Save file
            with open(file_path, "wb") as buffer:
                buffer.write(photo_content)
            
            # Update database
            photo_url = f"/static/uploads/photos/{unique_filename}"
            
            # Convert string to UUID
            try:
                registrant_uuid = UUID(registrant_id)
            except ValueError:
                # Clean up file if UUID is invalid
                try:
                    file_path.unlink()
                except Exception:
                    pass
                return False, "Invalid registrant ID", None
            
            async with AsyncSessionLocal() as session:
                result = await session.execute(
                    select(WebinarRegistrants).where(WebinarRegistrants.id == registrant_uuid)
                )
                registrant = result.scalar_one_or_none()
                
                if not registrant:
                    # Clean up file if registrant not found
                    try:
                        file_path.unlink()
                    except Exception:
                        pass
                    return False, "Registrant not found", None
                
                registrant.photo_url = photo_url
                await session.commit()
            
            return True, "Photo uploaded successfully!", photo_url
            
        except Exception as e:
            return False, f"Failed to save file: {str(e)}", None
    
    @staticmethod
    async def update_notes(registrant_id: str, notes: str) -> tuple[bool, str]:
        """
        Update notes for a webinar registrant
        
        Returns:
            tuple: (success, message)
        """
        try:
            # Convert string to UUID
            try:
                registrant_uuid = UUID(registrant_id)
            except ValueError:
                return False, "Invalid registrant ID"
            
            async with AsyncSessionLocal() as session:
                result = await session.execute(
                    select(WebinarRegistrants).where(WebinarRegistrants.id == registrant_uuid)
                )
                registrant = result.scalar_one_or_none()
                
                if not registrant:
                    return False, "Registrant not found"
                
                # Update database
                registrant.notes = notes
                await session.commit()
            
            return True, "Notes updated successfully!"
            
        except Exception as e:
            return False, f"Error updating notes: {str(e)}"
    
    @staticmethod
    async def delete_photo(registrant_id: str) -> tuple[bool, str]:
        """
        Delete a photo for a webinar registrant
        
        Returns:
            tuple: (success, message)
        """
        try:
            # Convert string to UUID
            try:
                registrant_uuid = UUID(registrant_id)
            except ValueError:
                return False, "Invalid registrant ID"
            
            async with AsyncSessionLocal() as session:
                result = await session.execute(
                    select(WebinarRegistrants).where(WebinarRegistrants.id == registrant_uuid)
                )
                registrant = result.scalar_one_or_none()
                
                if not registrant:
                    return False, "Registrant not found"
                
                if not registrant.photo_url:
                    return False, "No photo found for this registrant"
                
                # Delete file from filesystem
                photo_path = Path("static") / registrant.photo_url.lstrip("/static/")
                try:
                    if photo_path.exists():
                        photo_path.unlink()
                except Exception as e:
                    # Log error but don't fail the request
                    print(f"Failed to delete file {photo_path}: {e}")
                
                # Update database
                registrant.photo_url = None
                await session.commit()
            
            return True, "Photo deleted successfully!"
            
        except Exception as e:
            return False, f"Error deleting photo: {str(e)}" 