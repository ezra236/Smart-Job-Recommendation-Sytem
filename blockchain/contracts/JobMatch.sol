// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

contract JobMatch {
    struct Prediction {
        address user;
        string jobTitle;
        string reasoning;
        uint256 timestamp;
    }
    
    Prediction[] public predictions;
    // Track if an account has already made a prediction
    mapping(address => bool) public hasPredicted;
    
    event PredictionStored(address indexed user, string jobTitle, string reasoning, uint256 timestamp);

    function storePrediction(string memory _jobTitle, string memory _reasoning) public {
        // Ensure the sender has not already made a prediction
        require(!hasPredicted[msg.sender], "This account has already made a prediction.");
        
        // Store the prediction
        predictions.push(Prediction(msg.sender, _jobTitle, _reasoning, block.timestamp));
        hasPredicted[msg.sender] = true;
        
        emit PredictionStored(msg.sender, _jobTitle, _reasoning, block.timestamp);
    }

    function getPrediction(uint index) public view returns (address, string memory, string memory, uint256) {
        require(index < predictions.length, "Index out of range");
        Prediction memory pred = predictions[index];
        return (pred.user, pred.jobTitle, pred.reasoning, pred.timestamp);
    }

    function getPredictionCount() public view returns (uint) {
        return predictions.length;
    }
}
