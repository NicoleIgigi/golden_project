[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/S_OXTKjx)
## Summative Project: University Residence Management API

### Project Description

This capstone project tasks students with designing and developing a RESTful API for managing a university's residence system. This system will enable students and administrators to interact with various aspects of residence life, such as:

* Room applications and assignments
* Maintenance requests and tracking
* Event announcements and management
* Resident communication and feedback
* Administrative oversight and reporting

The API will be built using Django REST Framework, leveraging advanced Python concepts and techniques.

### [Stage-1: Foundation and Planning ](https://github.com/ALU-BSE/Summative-Project-UniNest-API/blob/stage-1/README.md) 
### [Stage-2: Enhanced Functionality](https://github.com/ALU-BSE/Summative-Project-UniNest-API/blob/stage-2/README.md) 
### [Stage-3: Advanced Features and Security](https://github.com/ALU-BSE/Summative-Project-UniNest-API/blob/stage-3/README.md) 
### [Stage-4: Testing and Refinement](https://github.com/ALU-BSE/Summative-Project-UniNest-API/blob/stage-4/README.md) 





Project Overview
The UniNest Residence Management API is designed to modernize the operations of UniNest, a leading university residence management company, by replacing their outdated paper-based system with a web-based platform. This API allows students and administrators to efficiently interact with the residence system in real-time across multiple devices.

Key Features:
Room Applications and Assignments: Enables students to apply for rooms, view application status, and accept/decline room offers.
Maintenance Requests: Allows students to submit, track, and rate maintenance requests.
Event Management: Facilitates the creation, registration, and management of residence events.
Resident Communication: Provides a messaging system for students and administrators.
Administrative Oversight and Reporting: Enables administrators to generate reports on various residence activities.
Payment Integration: Supports secure payment processing for rent and other fees.


 Business Rules and Requirements

 1. User Management
Students:
Room Management: Students can apply for rooms, view application status, accept or decline offers, and manage room assignments.
Maintenance Requests: Submit maintenance requests, track their progress, and provide feedback on the resolution.
Event Participation: Register for residence events, receive instant confirmations, and reminders.
Messaging System: Communicate with other residents and administrators via a secure messaging system.

Administrators:
Room Assignments: Manage student room allocations and assignments, handle waiting lists, and process room changes.
Maintenance Management: Review maintenance requests, assign them to staff, and provide real-time updates to students.
Event Management: Create, manage, and promote events within the residence.
Communication: Send announcements and notifications to all residents or specific groups.
Reporting: Generate reports on occupancy, maintenance requests, and other metrics relevant to residence management.

2. Room Management
Rooms are categorized by building, floor, type (single, double, etc.), and occupancy status.
Students can apply for rooms based on their preferences and eligibility.
Administrators manage room assignments, waiting lists, and room changes in real-time.

 3. Maintenance Requests
Students can submit requests, specifying details such as the issue, location, and urgency.
Administrators review and assign requests to maintenance staff, who update request statuses and completion notes.
Students receive real-time updates and can rate the service after resolution.

4. Events and Announcements
Event Creation: Administrators can create and manage events, view participant lists, and send reminders.
Event Participation: Students can register for events and receive instant confirmations.
Announcements: Administrators can send out important notifications to all or selected residents.

 5. Communication
 A secure messaging system enables residents to communicate with each other and with administrators.
Administrators can send mass messages or announcements to residents or target specific groups.

6. Data Integration
The API is designed to integrate with UniNest's existing databases and systems, which contain student information, room details, and maintenance history, ensuring seamless data transition and usage.

 7. Payment Integration
The platform integrates with a secure payment gateway for collecting rent and other fees. This ensures safe, encrypted transactions for both students and administrators.

 8. Analytics and Reporting
The API offers endpoints for generating reports and tracking metrics, such as occupancy rates, maintenance request trends, and event participation. These insights help administrators optimize residence management.
