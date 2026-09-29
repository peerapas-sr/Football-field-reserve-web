# Football Field Reservation Web

A full-stack web application designed for searching, scheduling, and reserving football and futsal fields online. The platform includes automated schedule tracking for users and an administrative management dashboard.

## Key Features

### For Users
* **Authentication and Authorization:** Secure sign-up, sign-in, and profile management.
* **Field Discovery:** Browse available fields, filter by surface type (natural grass, artificial turf) or pitch size (e.g., 5-a-side, 7-a-side, 11-a-side), and view amenities and hourly rates.
* **Real-Time Schedule Availability:** View an interactive calendar showing open and reserved time slots.
* **Booking System:** Select dates, times, and specific fields, calculate pricing automatically, and confirm reservations.
* **Booking History:** Track booking status (Pending, Confirmed, Cancelled).
* **Payment Slip Upload:** Attach proof of transfer/receipt directly upon booking.

### For Administrators
* **Overview Dashboard:** Monitor total reservations, occupancy rates, and revenue metrics.
* **Field Management:** Add, update, disable, or delete field profiles, pricing tiers, and maintenance schedules.
* **Reservation Control:** Review booking requests, verify payment slips, and approve or reject reservations.
* **User Management:** Manage accounts, access roles, and permissions.

## Tech Stack

> Note: Adjust these technologies to reflect your project's exact implementation.

* **Frontend:** HTML5, CSS3 / Tailwind CSS / Bootstrap, JavaScript (React / Vue.js / Vanilla JS)
* **Backend:** Node.js (Express) / PHP (Laravel) / Python (Django / FastAPI)
* **Database:** MySQL / PostgreSQL / MongoDB
* **Authentication:** JWT / Session-based authentication
* **Media Storage:** Local storage / Cloudinary / AWS S3

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/peerapas-sr/Football-field-reserve-web.git
cd Football-field-reserve-web
```

### 2. Install Dependencies

**For Node.js environments:**
```bash
npm install
# or
yarn install
```

**For PHP environments:**
```bash
composer install
```

### 3. Environment Configuration

Copy the example environment configuration file to `.env`:

```bash
cp .env.example .env
```

Configure your environment settings (database connection, application port, secret keys):

```env
PORT=5000
DATABASE_URL=mysql://root:password@localhost:3306/football_reservation
JWT_SECRET=your_jwt_secret_key
```

### 4. Database Setup and Migrations

Run database migrations to initialize tables and initial data:

```bash
# Node.js example:
npm run migrate

# PHP / Laravel example:
php artisan migrate
```

### 5. Run the Application

```bash
# Development server (Node.js):
npm run dev

# Development server (PHP):
php artisan serve
```

Access the application in your browser at `http://localhost:3000` or `http://localhost:8000`.

## Project Structure

```text
Football-field-reserve-web/
├── public/              # Static assets (images, stylesheets, icons)
├── src/                 # Application source code
│   ├── config/          # Database and service configurations
│   ├── controllers/     # Request handlers and business logic
│   ├── models/          # Database schemas and models
│   ├── routes/          # API endpoints and route definitions
│   ├── views/           # UI templates / components
│   └── middlewares/     # Authentication, upload, and error middlewares
├── .env.example         # Example configuration file
├── package.json         # Dependency manifest and scripts
└── README.md            # Project documentation
```

## Developer

* **GitHub:** [@peerapas-sr](https://github.com/peerapas-sr)
* **GitHub:** [@kittpong-so](https://github.com/kittipong-so)
* **GitHub:** [@dechawat-n](https://github.com/dechawat-n)
## License

This project is licensed under the [MIT License](LICENSE).
