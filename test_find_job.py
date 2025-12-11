#!/usr/bin/env python3
"""
Tests for Find Job - Automated Job Search Email System
"""
import os
import pytest
import json
from datetime import datetime
from find_job import FindJob


class TestFindJob:
    """Test cases for FindJob class"""
    
    @pytest.fixture
    def config_path(self, tmp_path):
        """Create a temporary test config file"""
        config_file = tmp_path / "test_config.yaml"
        config_content = """
job_search_prompt: |
  Please provide a brief list of 2 software engineering jobs for testing purposes.
  Keep the response short and simple.

openai_model: gpt-4
max_tokens: 500

email:
  smtp_server: smtp.gmail.com
  smtp_port: 587
  sender_email: test@example.com
  recipient_email: test@example.com
"""
        config_file.write_text(config_content)
        return str(config_file)
    
    @pytest.fixture
    def find_job_instance(self, config_path):
        """Create a FindJob instance with test config"""
        return FindJob(config_path)
    
    def test_search_jobs(self, find_job_instance):
        """
        Test the search_jobs function and print the OpenAI JSON response.
        
        This test calls the OpenAI API with a test prompt and prints:
        1. The full response object details
        2. The JSON representation of the response
        3. The content of the response
        """
        print("\n" + "="*80)
        print("TEST: search_jobs - Testing OpenAI API Integration")
        print("="*80)
        
        # Call the search_jobs function
        result = find_job_instance.search_jobs()
        
        # Get the actual OpenAI response for detailed output
        # We'll make another call to capture the full response object
        response = find_job_instance.openai_client.chat.completions.create(
            model=find_job_instance.config.get('openai_model', 'gpt-4'),
            messages=[
                {"role": "system", "content": "You are a helpful job search assistant. Provide job recommendations in a clear, structured format."},
                {"role": "user", "content": find_job_instance.config.get('job_search_prompt', '')}
            ],
            max_tokens=find_job_instance.config.get('max_tokens', 2000),
            temperature=0.7
        )
        
        # Print the OpenAI response in multiple formats
        print("\n--- OPENAI RESPONSE OBJECT DETAILS ---")
        print(f"Response ID: {response.id}")
        print(f"Model: {response.model}")
        print(f"Created: {datetime.fromtimestamp(response.created)}")
        print(f"Object Type: {response.object}")
        
        print("\n--- USAGE STATISTICS ---")
        print(f"Prompt Tokens: {response.usage.prompt_tokens}")
        print(f"Completion Tokens: {response.usage.completion_tokens}")
        print(f"Total Tokens: {response.usage.total_tokens}")
        
        print("\n--- CHOICE DETAILS ---")
        print(f"Finish Reason: {response.choices[0].finish_reason}")
        print(f"Message Role: {response.choices[0].message.role}")
        
        print("\n--- FULL JSON RESPONSE ---")
        # Convert the response to a dictionary format
        response_dict = {
            "id": response.id,
            "object": response.object,
            "created": response.created,
            "model": response.model,
            "choices": [
                {
                    "index": choice.index,
                    "message": {
                        "role": choice.message.role,
                        "content": choice.message.content
                    },
                    "finish_reason": choice.finish_reason
                }
                for choice in response.choices
            ],
            "usage": {
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens
            }
        }
        print(json.dumps(response_dict, indent=2))
        
        print("\n--- MESSAGE CONTENT ---")
        print(result)
        print("\n" + "="*80)
        
        # Assertions
        assert result is not None, "Result should not be None"
        assert len(result) > 0, "Result should not be empty"
        assert isinstance(result, str), "Result should be a string"
        
        print("\n✓ search_jobs test passed successfully!")
    
    def test_send_email(self, find_job_instance):
        """
        Test the send_email function by sending a plain test email.
        
        This test sends a simple test email to the configured recipient address.
        Note: This requires valid SMTP credentials in the .env file.
        """
        print("\n" + "="*80)
        print("TEST: send_email - Sending Test Email")
        print("="*80)
        
        # Create a simple test email content
        test_email_content = """
        <html>
            <head>
                <style>
                    body { font-family: Arial, sans-serif; }
                    .test-box { border: 2px solid #3498db; padding: 20px; margin: 20px; }
                </style>
            </head>
            <body>
                <div class="test-box">
                    <h1>Test Email</h1>
                    <p>This is a plain test email from the Find Job test suite.</p>
                    <p>Timestamp: {}</p>
                    <p>If you received this email, the send_email function is working correctly!</p>
                </div>
            </body>
        </html>
        """.format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        
        print("\n--- EMAIL CONFIGURATION ---")
        email_config = find_job_instance.config.get('email', {})
        print(f"SMTP Server: {email_config.get('smtp_server', os.getenv('SMTP_SERVER', 'Not configured'))}")
        print(f"SMTP Port: {email_config.get('smtp_port', os.getenv('SMTP_PORT', 'Not configured'))}")
        print(f"Sender Email: {email_config.get('sender_email', os.getenv('SENDER_EMAIL', 'Not configured'))}")
        print(f"Recipient Email: {email_config.get('recipient_email', os.getenv('RECIPIENT_EMAIL', 'Not configured'))}")
        
        print("\n--- SENDING EMAIL ---")
        try:
            find_job_instance.send_email(test_email_content)
            print("\n✓ Email sent successfully!")
            print("Check the recipient inbox to verify the test email was delivered.")
        except ValueError as e:
            print(f"\n⚠ Configuration Error: {e}")
            print("Please ensure SMTP credentials are set in .env file or config.yaml")
            pytest.skip(f"Skipping email test due to missing configuration: {e}")
        except Exception as e:
            print(f"\n✗ Error sending email: {e}")
            raise
        
        print("\n" + "="*80)


def test_load_config():
    """Test configuration loading from config.example.yaml"""
    print("\n" + "="*80)
    print("TEST: load_config - Testing Configuration Loading")
    print("="*80)
    
    # Use the example config file for testing
    find_job = FindJob('config.example.yaml')
    
    assert find_job.config is not None, "Config should be loaded"
    assert 'job_search_prompt' in find_job.config, "Config should have job_search_prompt"
    assert 'openai_model' in find_job.config, "Config should have openai_model"
    assert 'email' in find_job.config, "Config should have email configuration"
    
    print("\n✓ Configuration loaded successfully!")
    print(f"Model: {find_job.config['openai_model']}")
    print(f"Max Tokens: {find_job.config.get('max_tokens', 'default')}")
    print("\n" + "="*80)


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v", "-s"])
