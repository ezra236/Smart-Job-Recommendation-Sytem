// migrations/2_deploy.js
const JobMatch = artifacts.require("JobMatch");

module.exports = function (deployer) {
  deployer.deploy(JobMatch);
};
