import unittest
import base64
import json
import requests
from gozero_signature import GoZeroSigner

# Test keys from original Go code
PUBLIC_KEY = """-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCyeDYV2ieOtNDi6tuNtAbmUjN9
pTHluAU5yiKEz8826QohcxqUKP3hybZBcm60p+rUxMAJFBJ8Dt+UJ6sEMzrf1rOF
YOImVvORkXjpFU7sCJkhnLMs/kxtRzcZJG6ADUlG4GDCNcZpY/qELEvwgm2kCcHi
tGC2mO8opFFFHTR0aQIDAQAB
-----END PUBLIC KEY-----"""

KEY = "1234567890"

class TestSecuritySigner(unittest.TestCase):
    
    def test_generate_signature(self):
        signer = GoZeroSigner(PUBLIC_KEY, KEY)
        
        # Test payload similar to Go test
        payload = {"msg": "hello world!"}
        
        # Generate signature
        signature = signer.generate_signature(
            method="POST",
            url="http://127.0.0.1:8888/sign/demo",
            payload=payload
        )
        
        # Just verify it returns a string and has the expected format
        self.assertIsInstance(signature, str)
        self.assertTrue("key=" in signature)
        self.assertTrue("secret=" in signature)
        self.assertTrue("signature=" in signature)
        
        print(f"Generated signature: {signature}")

    def test_api_call(self):
        signer = GoZeroSigner(PUBLIC_KEY, KEY)
        
        # Test payload
        payload = {"msg": "hello world!"}
        
        # Generate signature
        signature = signer.generate_signature(
            method="POST",
            url="http://127.0.0.1:8888/sign/demo",
            payload=payload
        )
        
        # Prepare headers
        headers = {
            "Content-Type": "application/json",
            "X-Content-Security": signature
        }
        
        # Make the API call
        try:
            response = requests.post(
                "http://127.0.0.1:8888/sign/demo",
                json=payload,
                headers=headers
            )
            
            print(f"\nAPI Response Status Code: {response.status_code}")
            print(f"API Response Headers: {dict(response.headers)}")
            print(f"API Response Body: {response.text}")
            
            # Basic assertions
            self.assertIsInstance(response.status_code, int)
            
        except requests.exceptions.RequestException as e:
            print(f"\nError making API call: {str(e)}")
            self.fail(f"API call failed: {str(e)}")

    def test_get_signature(self):
        signer = GoZeroSigner(PUBLIC_KEY, KEY)
        signature = signer.generate_get_signature("http://127.0.0.1:8888/sign/get1?msg=123456")
        print(f"Generated signature: {signature}")
        self.assertIsInstance(signature, str)
        self.assertTrue("key=" in signature)
        self.assertTrue("secret=" in signature)
        self.assertTrue("signature=" in signature)

        try:
            response = requests.get(
                "http://127.0.0.1:8888/sign/get1?msg=123456",
                headers={"X-Content-Security": signature}
            )
            print(f"\nAPI Response Status Code: {response.status_code}")
            print(f"API Response Headers: {dict(response.headers)}")
            print(f"API Response Body: {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"\nError making API call: {str(e)}")
            self.fail(f"API call failed: {str(e)}")
        

if __name__ == "__main__":
    unittest.main()