# eKigega - Electronic Inventory Management System

## Project Overview
eKigega is a Django-based web application for inventory management. The name "eKigega" combines "electronic" with "ikigega," the traditional Kinyarwanda term for a storehouse.

## Objectives
- Develop a functional web application using Django, HTML, CSS, and AJAX
- Integrate cloud and distributed computing services
- Implement an inventory management system with CRUD operations

## Requirements

### Web Application
- Framework: Django
- Frontend: HTML, CSS, AJAX
- Features:
  - Authentication system (login/signup)
  - CRUD functionality for inventory items
  - Dashboard for analytics and reports

### Cloud Computing Integration
1. **MySQL Database on AWS**
   - Amazon RDS MySQL database named "ekigega"
   - Connected to Django application

2. **Hadoop (Local Machine or Cloud)**
   - MapReduce functionality for data processing
   - Data workflow: File upload to HDFS, MapReduce job execution
   - Results displayed on web application dashboard

3. **Kafka Integration**
   - Topic name: `inventory_updates`
   - Producer: `InventoryUpdateProducer` (publishes inventory changes)
   - Consumer: `InventoryUpdateConsumer` (consumes and displays real-time updates)
   - Actions:
     - When an item is added, updated, or deleted, the action is published to the `inventory_updates` topic
     - The consumer processes these messages and updates the dashboard in real-time

## Accessing the Project
1. Clone the repository:
   \`\`\`
   git clone https://github.com/Claudemuremyi/eKigega.git
   \`\`\`

## Local Machine Requirements
To run this project locally, you need the following installed:
- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)
- PostgreSQL
- Apache Kafka
- Hadoop (for local setup)

## Setting Up the Project
1. Create and activate a virtual environment:
   \`\`\`
   python -m venv env
   source env/bin/activate  # On Windows, use `env\Scripts\activate`
   \`\`\`
2. Install dependencies:
   \`\`\`
   pip install -r requirements.txt
   \`\`\`
3. Set up your local PostgreSQL database and update the `DATABASES` configuration in `settings.py`
4. Set up Kafka and ensure it's running locally
5. Configure Hadoop if you're running it locally
6. Run migrations:
   \`\`\`
   python manage.py migrate
   \`\`\`
7. Start the development server:
   \`\`\`
   python manage.py runserver
   \`\`\`

