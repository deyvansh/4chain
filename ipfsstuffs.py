import requests
import json
PINATA_JWT = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySW5mb3JtYXRpb24iOnsiaWQiOiIwYTA3MTk3ZS1jNDMzLTRiNDctODM2Mi1jOGIxMjI2M2YxMmYiLCJlbWFpbCI6ImFsaXNoYWphbWFsMTAwQGdtYWlsLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJwaW5fcG9saWN5Ijp7InJlZ2lvbnMiOlt7ImRlc2lyZWRSZXBsaWNhdGlvbkNvdW50IjoxLCJpZCI6IkZSQTEifSx7ImRlc2lyZWRSZXBsaWNhdGlvbkNvdW50IjoxLCJpZCI6Ik5ZQzEifV0sInZlcnNpb24iOjF9LCJtZmFfZW5hYmxlZCI6ZmFsc2UsInN0YXR1cyI6IkFDVElWRSJ9LCJhdXRoZW50aWNhdGlvblR5cGUiOiJzY29wZWRLZXkiLCJzY29wZWRLZXlLZXkiOiJjN2ViY2RkZmM5NDU0YzY1YTA5MSIsInNjb3BlZEtleVNlY3JldCI6ImE1YTU0MTM2OTQxMjQyOThmMjdkZmZjMzk4ZGM2MzE0NmQ5ZTQyYmZmMzIzN2JkZjRjZmVlYzVlYTdiZTliMGYiLCJleHAiOjE3OTAwMDg0NTd9.HQwHkvpGqIYfEgt91Ltpnv-LY6JZCtMfch9_6nDHaVQ"

def ipfs_upload(file_path):
    """Upload file to IPFS via Pinata API"""
    try:
        with open(file_path, 'rb') as file:
            files = {'file': (file_path, file)}
            headers = {
                'Authorization': f'Bearer {PINATA_JWT}'
            }
            
            response = requests.post(
                'https://api.pinata.cloud/pinning/pinFileToIPFS',
                files=files,
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                ipfs_hash = result['IpfsHash']
                return f"https://ipfs.io/ipfs/{ipfs_hash}"
            else:
                print(f"Pinata upload failed: {response.text}")
               
                return f"https://ipfs.io/ipfs/QmDemo123{file_path[-8:]}"
                
    except Exception as e:
        print(f"IPFS upload error: {str(e)}")
    
        return f"https://ipfs.io/ipfs/QmDemo123{file_path[-8:]}"

def test_pinata_connection():
    """Test if Pinata API is working"""
    try:
        headers = {
            'Authorization': f'Bearer {PINATA_JWT}'
        }
        response = requests.get(
            'https://api.pinata.cloud/data/testAuthentication',
            headers=headers
        )
        return response.status_code == 200
    except:
        return False
