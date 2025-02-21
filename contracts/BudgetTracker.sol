// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract BudgetTracker {
    struct Department {
        string name;
        uint256 allocatedBudget;
        uint256 spentBudget;
    }

    address public admin;
    mapping(uint256 => Department) public departments;
    uint256 public departmentCount;

    event BudgetAllocated(uint256 departmentId, string name, uint256 amount);
    event BudgetSpent(uint256 departmentId, uint256 amount);

    modifier onlyAdmin() {
        require(msg.sender == admin, "Only admin can perform this action");
        _;
    }

    constructor() {
        admin = msg.sender;
    }

    function allocateBudget(uint256 departmentId, string memory name, uint256 amount) public onlyAdmin {
        departments[departmentId] = Department(name, amount, 0);
        departmentCount++;
        emit BudgetAllocated(departmentId, name, amount);
    }

    function spendBudget(uint256 departmentId, uint256 amount) public onlyAdmin {
        require(departments[departmentId].allocatedBudget >= departments[departmentId].spentBudget + amount, "Exceeds allocated budget");
        departments[departmentId].spentBudget += amount;
        emit BudgetSpent(departmentId, amount);
    }

    function getDepartment(uint256 departmentId) public view returns (string memory, uint256, uint256) {
        Department memory department = departments[departmentId];
        return (department.name, department.allocatedBudget, department.spentBudget);
    }
}
