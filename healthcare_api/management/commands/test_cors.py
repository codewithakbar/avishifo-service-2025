from django.core.management.base import BaseCommand
from django.test import Client
from django.conf import settings


class Command(BaseCommand):
    help = 'Test CORS configuration'

    def handle(self, *args, **options):
        self.stdout.write("Testing CORS configuration...")
        
        client = Client()
        
        # Test OPTIONS request
        response = client.options(
            '/api/chat/gpt/chats/1/send_message/',
            HTTP_ORIGIN='https://dashboard.avishifo.uz',
            HTTP_ACCESS_CONTROL_REQUEST_METHOD='POST',
            HTTP_ACCESS_CONTROL_REQUEST_HEADERS='Content-Type, Authorization'
        )
        
        self.stdout.write(f"OPTIONS request status: {response.status_code}")
        
        # Check CORS headers
        cors_headers = {
            'Access-Control-Allow-Origin': response.get('Access-Control-Allow-Origin'),
            'Access-Control-Allow-Methods': response.get('Access-Control-Allow-Methods'),
            'Access-Control-Allow-Headers': response.get('Access-Control-Allow-Headers'),
            'Access-Control-Allow-Credentials': response.get('Access-Control-Allow-Credentials'),
        }
        
        self.stdout.write("CORS headers:")
        for header, value in cors_headers.items():
            if value:
                self.stdout.write(f"  {header}: {value}")
            else:
                self.stdout.write(f"  {header}: MISSING")
        
        # Check if CORS is properly configured
        if cors_headers['Access-Control-Allow-Origin']:
            self.stdout.write(
                self.style.SUCCESS("✅ CORS configuration appears to be working!")
            )
        else:
            self.stdout.write(
                self.style.ERROR("❌ CORS configuration needs attention!")
            )
