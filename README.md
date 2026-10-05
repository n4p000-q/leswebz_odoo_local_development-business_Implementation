LESWEBZ Odoo Local Development & Business Implementation
Overview

This project contains a local Odoo 19 development environment with PostgreSQL and a custom Guest House module.

The implementation includes two separate Odoo databases:

thimo_guesthouse, Guest House booking and room workflow
vishanti_bakery, Bakery Inventory, Purchase, Manufacturing and Point of Sale workflow
Requirements
Docker
Docker Compose
Git
Odoo 19
PostgreSQL 15
Project Structure
leswebz/
├── addons/
│   └── thimo_guesthouse/
├── config/
│   └── odoo.conf.example
├── docker-compose.yml
├── .gitignore
└── README.md
Local Setup
1. Clone the repository
git clone <REPOSITORY_URL>
cd leswebz
2. Create the local environment file

Create .env:

POSTGRES_USER=****
POSTGRES_PASSWORD=****
3. Create the local Odoo configuration

Copy the example configuration:

cp config/odoo.conf.example config/odoo.conf

Edit config/odoo.conf and set the local administrator and database credentials.

4. Start Odoo and PostgreSQL
docker compose up -d

Check the containers:

docker compose ps

Odoo is available at:

http://localhost:8069
5. Create the databases

Create the following databases through Odoo:

thimo_guesthouse
vishanti_bakery

Enable Developer Mode when required.

Database A - Thimo & Sons Guest House

Database:

thimo_guesthouse

The custom thimo_guesthouse module provides the Guest House booking workflow.

Configured Data

Room types:

Single - 500 LSL/night
Double - 750 LSL/night
Family - 1000 LSL/night

Rooms:

101 — Single
102 — Single
201 — Double
202 — Double
301 — Family

Guests:

Napo Qheku
Thakane Rampuku
Katleho Seutloali
Thabo Mbeki

Booking Workflow

The implemented workflow is:

Booking → Check-in → Check-out

The room status changes according to the booking workflow.

The demonstration data includes bookings with different dates and statuses, including:

Checked Out
Checked In
Confirmed

Database B - Vishanti Bakery

Database:

vishanti_bakery

The following Odoo applications are configured:

Inventory
Purchase
Manufacturing
Point of Sale
Products

Ingredients:

Flour
Sugar
Yeast

Finished product:

Croissant

Additional purchased product:

Coca-Cola 1L
Croissant Manufacturing Workflow

The Croissant Bill of Materials contains:

0.10 kg Flour
0.02 kg Sugar
0.005 kg Yeast

The workflow is:

Ingredient Stock
      ↓
Manufacturing Order
      ↓
Produce Croissant
      ↓
Croissant Stock
      ↓
POS Sale

Manufacturing decreases the ingredient stock and increases finished Croissant stock. Selling the Croissant through POS decreases the finished-product stock.

Coca-Cola Purchase Workflow

The workflow is:

Purchase Order
      ↓
Receive Products
      ↓
Inventory Stock
      ↓
POS Sale
      ↓
Reduced Inventory Stock

A quantity of 10 Coca-Cola 1L units was received into inventory.

One unit was subsequently sold through POS, resulting in:

Before POS sale: 10
After POS sale:   9
Custom Module

The custom Guest House module is located at:

addons/thimo_guesthouse/

Odoo loads custom modules from:

/mnt/extra-addons

The Docker Compose configuration mounts the local addons/ directory into this location.

Restarting the Environment

To stop the environment:

docker compose down

To start it again:

docker compose up -d

To restart the running containers:

docker compose restart

Check status with:

docker compose ps

Then open:

http://localhost:8069

The PostgreSQL and Odoo data are stored in Docker volumes so the databases persist across container restarts.
