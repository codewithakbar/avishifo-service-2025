from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin


class CustomCorsMiddleware(MiddlewareMixin):
    """
    Custom CORS middleware to handle preflight requests and add CORS headers
    """
    
    def process_request(self, request):
        # Handle preflight OPTIONS requests
        if request.method == 'OPTIONS':
            response = JsonResponse({})
            self.add_cors_headers(response, request)
            return response
        return None
    
    def process_response(self, request, response):
        # Add CORS headers to all responses
        self.add_cors_headers(response, request)
        return response
    
    def add_cors_headers(self, response, request):
        """Add CORS headers to response"""
        origin = request.META.get('HTTP_ORIGIN')
        
        # Allow specific origins
        allowed_origins = [
            'https://dashboard.avishifo.uz',
            'https://new.avishifo.uz',
            'https://avishifo.uz',
            'http://localhost:3000',
            'http://127.0.0.1:3000',
        ]
        
        # Check if origin is allowed or matches pattern
        if origin and (origin in allowed_origins or origin.endswith('.avishifo.uz')):
            response['Access-Control-Allow-Origin'] = origin
        else:
            response['Access-Control-Allow-Origin'] = '*'
        
        response['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS, PATCH'
        response['Access-Control-Allow-Headers'] = (
            'Content-Type, Authorization, X-Requested-With, '
            'Accept, Origin, X-CSRFToken, Cache-Control, Pragma'
        )
        response['Access-Control-Allow-Credentials'] = 'true'
        response['Access-Control-Max-Age'] = '86400'
        response['Access-Control-Expose-Headers'] = 'Content-Type, X-CSRFToken'
        
        return response
