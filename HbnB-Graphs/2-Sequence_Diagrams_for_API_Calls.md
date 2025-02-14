```mermaid
sequenceDiagram
    participant User
    participant API
    participant BusinessLogic
    participant Database

    User->>API: Register User
    API->>BusinessLogic: Validate User Data
    BusinessLogic->>Database: Store User Information
    Database-->>BusinessLogic: Confirmation
    BusinessLogic-->>API: User Created Response
    API-->>User: Success/Failure Message

    User->>API: Create New Place
    API->>BusinessLogic: Validate Place Data
    BusinessLogic->>Database: Store Place Information
    Database-->>BusinessLogic: Confirmation
    BusinessLogic-->>API: Place Created Response
    API-->>User: Success/Failure Message

    User->>API: Submit Review
    API->>BusinessLogic: Validate Review Data
    BusinessLogic->>Database: Store Review
    Database-->>BusinessLogic: Confirmation
    BusinessLogic-->>API: Review Submitted Response
    API-->>User: Success/Failure Message

    User->>API: Fetch List of Places
    API->>BusinessLogic: Retrieve Places Based on Criteria
    BusinessLogic->>Database: Fetch Matching Places
    Database-->>BusinessLogic: Return Place Data
    BusinessLogic-->>API: Send Place Data
    API-->>User: Return List of Places

