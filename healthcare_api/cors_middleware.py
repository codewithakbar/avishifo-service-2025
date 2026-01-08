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
        """Add CORS headers to response - allows all origins"""
        origin = request.META.get('HTTP_ORIGIN')
        
        # Allow all origins - echo back the origin if provided
        # When credentials are enabled, we MUST echo back the exact origin (cannot use *)
        if origin:
            response['Access-Control-Allow-Origin'] = origin
            response['Access-Control-Allow-Credentials'] = 'true'
        else:
            # No origin header means it's likely a same-origin request
            # Set * for non-credential requests, but don't set credentials
            response['Access-Control-Allow-Origin'] = '*'
        
        response['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS, PATCH'
        response['Access-Control-Allow-Headers'] = (
            'Content-Type, Authorization, X-Requested-With, '
            'Accept, Origin, X-CSRFToken, Cache-Control, Pragma'
        )
        response['Access-Control-Max-Age'] = '86400'
        response['Access-Control-Expose-Headers'] = 'Content-Type, X-CSRFToken'
        
        return response
