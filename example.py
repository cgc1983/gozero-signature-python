from gozero_signature import GoZeroSigner
import requests
import json

def main():
    """
    Example of using the GoZeroSigner for both GET and POST requests.
    """
    # Your RSA public key
    public_key = """-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCyeDYV2ieOtNDi6tuNtAbmUjN9
pTHluAU5yiKEz8826QohcxqUKP3hybZBcm60p+rUxMAJFBJ8Dt+UJ6sEMzrf1rOF
YOImVvORkXjpFU7sCJkhnLMs/kxtRzcZJG6ADUlG4GDCNcZpY/qELEvwgm2kCcHi
tGC2mO8opFFFHTR0aQIDAQAB
-----END PUBLIC KEY-----"""

    # Your secret key (can be base64 encoded or plain text)
    key = "1234567890"

    # Create a signer instance
    signer = GoZeroSigner(public_key, key)

    # Example 1: POST request
    print("\n=== Example 1: POST Request ===")
    payload = {"msg": "hello world!"}
    post_url = "http://127.0.0.1:8888/sign/demo"
    
    # Generate the signature header for POST
    post_signature = signer.generate_post_signature(
        url=post_url,
        payload=payload
    )

    print(f"Generated X-Content-Security header for POST: {post_signature}")
    
    # Example POST request
    post_headers = {
        "Content-Type": "application/json",
        "X-Content-Security": post_signature
    }
    
    try:
        post_response = requests.post(
            post_url,
            json=payload,
            headers=post_headers
        )
        print(f"POST Response Status: {post_response.status_code}")
        print(f"POST Response Body: {post_response.text}")
    except requests.exceptions.RequestException as e:
        print(f"POST Request Error: {str(e)}")

    # Example 2: GET request
    print("\n=== Example 2: GET Request ===")
    get_url = "http://127.0.0.1:8888/sign/get1?msg=123456"
    
    # Generate the signature header for GET
    get_signature = signer.generate_get_signature(get_url)
    
    print(f"Generated X-Content-Security header for GET: {get_signature}")
    
    # Example GET request
    get_headers = {
        "X-Content-Security": get_signature
    }
    
    try:
        get_response = requests.get(
            get_url,
            headers=get_headers
        )
        print(f"GET Response Status: {get_response.status_code}")
        print(f"GET Response Body: {get_response.text}")
    except requests.exceptions.RequestException as e:
        print(f"GET Request Error: {str(e)}")


if __name__ == "__main__":
    main()