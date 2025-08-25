from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponse, JsonResponse
import json


class CustomCorsMiddleware(MiddlewareMixin):
    """
    Custom CORS middleware to ensure proper CORS headers are set
    for all endpoints, especially the chat API endpoints.
    """
    
    def process_request(self, request):
        """Handle preflight OPTIONS requests"""
        if request.method == "OPTIONS":
            response = HttpResponse()
            response["Access-Control-Allow-Origin"] = "https://dashboard.avishifo.uz"
            response["Access-Control-Allow-Credentials"] = "true"
            response["Access-Control-Allow-Methods"] = "GET, POST, PUT, PATCH, DELETE, OPTIONS"
            response["Access-Control-Allow-Headers"] = "Content-Type, Authorization, X-Requested-With, Accept, Origin"
            response["Access-Control-Max-Age"] = "86400"
            return response
        return None
    
    def process_response(self, request, response):
        """Set CORS headers for all responses"""
        
        # Set CORS headers for all responses
        response["Access-Control-Allow-Origin"] = "https://dashboard.avishifo.uz"
        response["Access-Control-Allow-Credentials"] = "true"
        response["Access-Control-Allow-Methods"] = "GET, POST, PUT, PATCH, DELETE, OPTIONS"
        response["Access-Control-Allow-Headers"] = "Content-Type, Authorization, X-Requested-With, Accept, Origin"
        
        # Special handling for chat API endpoints
        if "/api/chat/" in request.path:
            response["Access-Control-Allow-Origin"] = "https://dashboard.avishifo.uz"
            response["Access-Control-Allow-Credentials"] = "true"
            response["Access-Control-Allow-Methods"] = "GET, POST, PUT, PATCH, DELETE, OPTIONS"
            response["Access-Control-Allow-Headers"] = "Content-Type, Authorization, X-Requested-With, Accept, Origin"
            response["Access-Control-Max-Age"] = "86400"
        
        return response
