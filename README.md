# IS212-g4t1 SBRP
## G4T1

## Prerequisites

Before you begin, ensure you have the following prerequisites:

- Node.js and npm (Node Package Manager) installed on your machine.

## Installation

1. Clone this repository to your local machine:  
  ```
  git clone https://github.com/xuanli286/IS212-g4t1.git
  ```

3. Change the working directory to your project folder:  
  ```
  cd IS212-g4t1
  ```

5. Install frontend project dependencies:
  ```
  cd frontend
  npm install
  ```  

7. Install backend project dependencies:
  ```
  cd..
  cd backend
  pip install -r requirements.txt
  ```

8. Set up backend environment  
  **Option 1** : AWS EC2 (set up Continuous Development)  
  Follow steps in [CD Documentation](https://docs.google.com/document/d/1g4fEYBYLkMK1JdJ0Rc-Ovfa3eD7IXG25xN-9f-8slTE/edit?usp=sharing)  
  **Option 2**: Local database environment
   Follow steps in [Local Backend Documentation](https://docs.google.com/document/d/1TLUOgL72Z1CxHkzniq_yQ9lF1X6Rhm28illRnb1LxyM/edit)
   > Notes: </br>
   > Make sure your working directory is IS212-g4t1/backend  </br>
   > <b>Make sure frontend/src/store/useConstStore.js line 12 is commented out and line 13 uncommented. This switches the database environment from AWS EC2 to local.</b>
   ```
   cd production_backend
   python g4t1.py
   ```

   
## Pytest and Selenium Tests

### Set up testing environment
#### **Option 1** : AWS EC2 (set up Continuous Development)
Follow steps in [CD Documentation](https://docs.google.com/document/d/1g4fEYBYLkMK1JdJ0Rc-Ovfa3eD7IXG25xN-9f-8slTE/edit?usp=sharing)  
> Note: Tests are currently using AWS backend links. Replace links if different.

#### **Option 2**: Local testing environment
Follow steps in [Local Backend Documentation](https://docs.google.com/document/d/1TLUOgL72Z1CxHkzniq_yQ9lF1X6Rhm28illRnb1LxyM/edit)  
> Note: Replace backend links to local environment links.

### How to edit backend links
1. Find conftest.py file, directory -> IS212-g4t1/backend/tests/conftest.py  
2. Replace `backend_base_url` & `backend_base_url_production`  

### Run Tests
#### **Option 1**: Run every tests
1. Change working directory to frontend
  ```
  cd frontend
  ```  

3. Run all tests using NPM
  ```
  npm run test
  ```  

#### **Option 2**: Run specific test file
1. Change working directory to tests
  ```
  cd backend/tests
  ```  

3. Run all tests using Pytest
  ```
  pytest test_IG_<User Story Issue Key>.py
  ```  








