import ipfshttpclient
import requests

PINATA_JWT = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySW5mb3JtYXRpb24iOnsiaWQiOiIwYTA3MTk3ZS1jNDMzLTRiNDctODM2Mi1jOGIxMjI2M2YxMmYiLCJlbWFpbCI6ImFsaXNoYWphbWFsMTAwQGdtYWlsLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJwaW5fcG9saWN5Ijp7InJlZ2lvbnMiOlt7ImRlc2lyZWRSZXBsaWNhdGlvbkNvdW50IjoxLCJpZCI6IkZSQTEifSx7ImRlc2lyZWRSZXBsaWNhdGlvbkNvdW50IjoxLCJpZCI6Ik5ZQzEifV0sInZlcnNpb24iOjF9LCJtZmFfZW5hYmxlZCI6ZmFsc2UsInN0YXR1cyI6IkFDVElWRSJ9LCJhdXRoZW50aWNhdGlvblR5cGUiOiJzY29wZWRLZXkiLCJzY29wZWRLZXlLZXkiOiJjN2ViY2RkZmM5NDU0YzY1YTA5MSIsInNjb3BlZEtleVNlY3JldCI6ImE1YTU0MTM2OTQxMjQyOThmMjdkZmZjMzk4ZGM2MzE0NmQ5ZTQyYmZmMzIzN2JkZjRjZmVlYzVlYTdiZTliMGYiLCJleHAiOjE3OTAwMDg0NTd9.HQwHkvpGqIYfEgt91Ltpnv-LY6JZCtMfch9_6nDHaVQ"
PINATA_BASE_URL = "https://api.pinata.cloud/pinning/pinFileToIPFS"

def ipfs_upload(filepath):
    headers = {"Authorization": f"Bearer {PINATA_JWT}"}
    with open(filepath, "rb") as fp:
        files = {"file": fp}
        response = requests.post(PINATA_BASE_URL, files=files, headers=headers)
    if response.status_code == 200:
        ipfs_hash = response.json()["IpfsHash"]
        return f"https://gateway.pinata.cloud/ipfs/{ipfs_hash}"
    else:
        raise Exception(f"Failed to upload to pinata: {response.text}")

    


