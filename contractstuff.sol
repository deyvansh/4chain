// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract CertificateVerification {
    
    struct Certificate {
        string hash;
        uint256 timestamp;
        bool exists;
    }
    
    mapping(string => Certificate) public certificates;
    address public owner;
    
    event CertificateStored(string indexed cid, string hash, uint256 timestamp);
    
    modifier onlyOwner() {
        require(msg.sender == owner, "Only owner can perform this action");
        _;
    }
    
    constructor() {
        owner = msg.sender;
    }
    
    function storeCertificate(string memory _cid, string memory _hash) public onlyOwner {
        require(!certificates[_cid].exists, "Certificate already exists");
        
        certificates[_cid] = Certificate({
            hash: _hash,
            timestamp: block.timestamp,
            exists: true
        });
        
        emit CertificateStored(_cid, _hash, block.timestamp);
    }
    
    function verifyCertificate(string memory _cid) public view returns (bool, string memory) {
        Certificate memory cert = certificates[_cid];
        return (cert.exists, cert.hash);
    }
    
    function getCertificateTimestamp(string memory _cid) public view returns (uint256) {
        require(certificates[_cid].exists, "Certificate does not exist");
        return certificates[_cid].timestamp;
    }
    
    function changeOwner(address _newOwner) public onlyOwner {
        owner = _newOwner;
    }
}
