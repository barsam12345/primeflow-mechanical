# PrimeFlow Mechanical Website

A professional website for PrimeFlow Mechanical, featuring HVAC and plumbing services with an admin panel for managing quote requests.

## Features

- **Modern, Responsive Design**: Beautiful website with mobile-friendly layout
- **Quote Request System**: Customers can submit quote requests through a form
- **Email Notifications**: Automatic email alerts for new quote requests
- **Admin Panel**: Secure admin interface to manage quote requests
- **Real-time Updates**: Auto-refreshing dashboard with live statistics
- **Database Storage**: SQLite database for storing quote requests
- **Security Features**: Rate limiting, helmet security, bcrypt password hashing

## Quick Start

### Prerequisites

- Node.js 14.0 or higher
- npm (Node package manager)

### Installation

1. **Clone or download the project files**

2. **Install Node.js dependencies**:
   ```bash
   npm install
   ```

3. **Run the server**:
   ```bash
   npm start
   ```
   
   Or for development with auto-restart:
   ```bash
   npm run dev
   ```

4. **Access the website**:
   - Main website: http://localhost:3000
   - Admin panel: http://localhost:3000/admin
   - Admin login: `admin` / `admin123`

## File Structure

```
├── server.js              # Node.js/Express backend server
├── package.json           # Node.js dependencies and scripts
├── README.md              # This file
├── public/                # Website files
│   ├── index.html         # Main website
│   └── admin.html         # Admin panel
└── primeflow.db           # SQLite database (created automatically)
```

## Website Features

### Main Website (`/`)
- Professional landing page with hero section
- Services showcase (HVAC, Plumbing, Maintenance, etc.)
- Quote request form with validation
- Contact information and footer

### Admin Panel (`/admin`)
- Secure login system with bcrypt password hashing
- Dashboard with statistics
- Quote request management
- Status updates (Pending, Contacted, Completed, Cancelled)
- Real-time data refresh

## API Endpoints

- `POST /api/quote` - Submit a new quote request
- `POST /admin/login` - Admin login
- `POST /admin/logout` - Admin logout
- `GET /admin/quotes` - Get all quote requests (admin only)
- `PUT /admin/quotes/:id` - Update quote status (admin only)

## Email Configuration

To enable email notifications for new quote requests, configure your email settings:

1. **Set environment variables**:
   ```bash
   export EMAIL_USER="your-email@gmail.com"
   export EMAIL_PASS="your-app-password"
   ```

2. **For Gmail**, you'll need to:
   - Enable 2-factor authentication
   - Generate an "App Password"
   - Use the app password instead of your regular password

3. **Update the recipient email** in `server.js`:
   ```javascript
   to: 'quotes@primeflowmechanical.com', // Your business email
   ```

## Database Schema

The application uses SQLite with the following table structure:

```sql
-- Quotes table
CREATE TABLE quotes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    phone TEXT NOT NULL,
    service_area TEXT NOT NULL,
    service_type TEXT NOT NULL,
    message TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    status TEXT DEFAULT 'pending'
);

-- Admin users table
CREATE TABLE admin_users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

## Security Features

- **Helmet**: Security headers for protection against common vulnerabilities
- **Rate Limiting**: Prevents abuse with 100 requests per 15 minutes per IP
- **Bcrypt**: Secure password hashing for admin accounts
- **Session Management**: Secure session handling for admin authentication
- **Input Validation**: Server-side validation for all form inputs

## Customization

### Changing Admin Credentials
The default admin user is created automatically. To change credentials:

1. **Delete the database file** (`primeflow.db`)
2. **Update the default password** in `server.js`:
   ```javascript
   const defaultPassword = bcrypt.hashSync('your-new-password', 10);
   ```
3. **Restart the server**

### Modifying Services
Update the services section in `public/index.html` to match your business offerings.

### Styling
The website uses a gold/bronze color scheme (`#bfa046`). You can modify the CSS variables in both HTML files to match your brand colors.

## Environment Variables

- `PORT` - Server port (default: 3000)
- `EMAIL_USER` - Email address for sending notifications
- `EMAIL_PASS` - Email password/app password

## Production Deployment

For production deployment, consider:

1. **Using a process manager** (PM2):
   ```bash
   npm install -g pm2
   pm2 start server.js --name "primeflow"
   ```

2. **Setting up a reverse proxy** (Nginx):
   ```nginx
   server {
       listen 80;
       server_name yourdomain.com;
       
       location / {
           proxy_pass http://localhost:3000;
           proxy_http_version 1.1;
           proxy_set_header Upgrade $http_upgrade;
           proxy_set_header Connection 'upgrade';
           proxy_set_header Host $host;
           proxy_cache_bypass $http_upgrade;
       }
   }
   ```

3. **Using environment variables** for configuration
4. **Implementing proper SSL/TLS certificates**
5. **Setting up database backups**
6. **Adding monitoring and logging**

## Development

For development with auto-restart:
```bash
npm run dev
```

This uses nodemon to automatically restart the server when files change.

## Support

For questions or issues, please check the code comments or create an issue in the repository.

---

**PrimeFlow Mechanical** - Professional HVAC & Plumbing Services 