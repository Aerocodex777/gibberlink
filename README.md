# GibberLink 🔗

A modern web application for creating gibberlink messages. Built with Python backend and responsive web interface.

## 🌟 Features

- **🎨 Custom Aliases** - Create custom short codes for your links
- **📱 Responsive Design** - Works seamlessly on desktop, tablet, and mobile devices
- **🔒 Link Management** - Edit, delete, and manage your shortened links
- **📈 Dashboard** - View statistics and performance metrics for all your links
- **🌍 Global Access** - Share links that work anywhere in the world
- **⚙️ Easy Integration** - Simple API for programmatic URL shortening

## 🛠️ Tech Stack

### Backend
- **Python** - Backend language
- **Framework**: Flask (lightweight web framework)
- **Database**: SQLite/PostgreSQL (configurable)
- **ORM**: SQLAlchemy for database operations

### Frontend
- **HTML5** - Semantic markup
- **CSS3** - Modern styling with responsive design
- **JavaScript** - Interactive features and real-time updates
- **Bootstrap/Tailwind** - UI framework for beautiful layouts

### Infrastructure
- **Server**: Gunicorn/uWSGI
- **Database**: SQLite (development), PostgreSQL (production)
- **Hosting**: Heroku, AWS, or any Python-compatible host

## 📁 Project Structure

```
gibberlink/
├── gibber.py              # Main Flask application
├── requirements.txt       # Python dependencies
├── template/              # HTML templates
│   ├── inter.html        # Main interface
│   └── gibberli/         # Additional templates
├── static/               # CSS, JavaScript, images
├── models/               # Database models
└── README.md            # This file
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Virtual environment (recommended)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Aerocodex777/gibberlink.git
   cd gibberlink
   ```

2. **Create virtual environment**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate
   
   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python gibber.py
   ```

5. **Open in browser**
   - Navigate to `http://localhost:5000`

## 💡 How It Works

### URL Shortening Process

```
Long URL Input
    ↓
Validation & Check
    ↓
Generate Short Code (or use custom)
    ↓
Store in Database
    ↓
Return Short Link
```

### Link Redirect Flow

```
User clicks short link
    ↓
Server retrieves mapping
    ↓
Log analytics (time, referrer, IP)
    ↓
Redirect to original URL
    ↓
Increment click counter
```

## 📊 API Endpoints

### GET `/`
Returns the main web interface for URL shortening.

### POST `/shorten`
Create a new shortened URL.

**Request:**
```json
{
  "original_url": "https://example.com/very/long/url",
  "custom_alias": "mylink"  # optional
}
```

**Response:**
```json
{
  "success": true,
  "short_code": "abc123",
  "short_url": "https://gibberlink.com/abc123",
  "original_url": "https://example.com/very/long/url",
  "created_at": "2025-12-04T10:30:00Z"
}
```

### GET `/<short_code>`
Redirect to the original URL.

**Response:**
- HTTP 301 Redirect to original URL
- Logs analytics data

### GET `/api/stats/<short_code>`
Get analytics for a specific shortened link.

**Response:**
```json
{
  "short_code": "abc123",
  "original_url": "https://example.com/...",
  "clicks": 142,
  "created_at": "2025-12-04T10:30:00Z",
  "top_referrers": ["google.com", "twitter.com"],
  "recent_clicks": [
    {
      "timestamp": "2025-12-04T15:45:00Z",
      "referrer": "google.com",
      "user_agent": "Mozilla/5.0...",
      "ip": "192.168.1.1"
    }
  ]
}
```

### DELETE `/api/link/<short_code>`
Delete a shortened link.

**Response:**
```json
{
  "success": true,
  "message": "Link deleted successfully"
}
```

## 🎯 Use Cases

- **Social Media Sharing** - Create clean, shareable links for Twitter, LinkedIn, etc.
- **Marketing Campaigns** - Track campaign performance with link analytics
- **QR Codes** - Generate QR codes from shortened links for offline use
- **Email Marketing** - Include tracked links in marketing emails
- **Blog Sharing** - Share articles with neat, short URLs
- **Document Sharing** - Create memorable links to important files
- **Event Promotion** - Track registrations and interest with link analytics

## ⚙️ Configuration

Create a `.env` file in the project root:

```env
FLASK_ENV=production
DATABASE_URL=postgresql://user:password@localhost/gibberlink
SECRET_KEY=your-secret-key-here
DOMAIN=gibberlink.com
DEBUG=False
PORT=5000
MAX_URL_LENGTH=2048
```

## 📈 Features in Detail

### Custom Aliases
- Create memorable short codes: `gb.link/myproject`
- Check availability before creating
- Prevent duplicate aliases

### Analytics Dashboard
- Real-time click tracking
- Geographic data (if available)
- Referrer analysis
- Device and browser information
- Time-based trends

### URL Validation
- Check for valid URLs
- Prevent malicious URLs
- Handle URL encoding
- Duplicate URL detection

## 🔒 Security

✅ **URL Validation** - Prevent malicious URLs
✅ **Rate Limiting** - Prevent spam and abuse
✅ **SQL Injection Prevention** - Using ORM and parameterized queries
✅ **HTTPS Support** - Encrypted communication
✅ **CORS Protection** - Cross-origin request security

## 📦 Dependencies

Key packages (see `requirements.txt` for complete list):
- Flask 2.3.3+
- SQLAlchemy
- requests
- python-dotenv
- Werkzeug

## 🚀 Deployment

### Deploy to Heroku

1. Create `Procfile`:
   ```
   web: gunicorn gibber:app
   ```

2. Create `runtime.txt`:
   ```
   python-3.11.4
   ```

3. Deploy:
   ```bash
   heroku create your-app-name
   heroku config:set SECRET_KEY=your-secret-key
   git push heroku main
   ```

### Deploy to AWS
- Use AWS Lambda with Flask API
- RDS for database
- CloudFront for CDN

### Deploy to DigitalOcean
- Create Droplet
- Install Python and dependencies
- Use Nginx reverse proxy
- Supervisor for process management

## 🔧 Troubleshooting

### Port Already in Use
```bash
# Change port in gibber.py or use environment variable
export PORT=5001
python gibber.py
```

### Database Connection Error
- Check DATABASE_URL in `.env`
- Verify database is running
- Check credentials

### Short Code Generation Collision
- Uses UUID or incremental counters
- Handles duplicates automatically
- Retries if collision detected

## 📚 Learning Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLAlchemy ORM](https://docs.sqlalchemy.org/)
- [URL Shortening Best Practices](https://en.wikipedia.org/wiki/URL_shortening)
- [REST API Design](https://restfulapi.net/)

## 🤝 Contributing

Contributions are welcome! Areas for improvement:
- QR code generation integration
- Advanced analytics dashboard
- Bulk URL shortening
- API key management for developers
- Custom domain support
- Link expiration dates
- Password-protected links

## 📝 License

This project is open source and available under the MIT License.

## 👨‍💻 Author

Created by **Aerocodex777**

---

**Repository**: [https://github.com/Aerocodex777/gibberlink](https://github.com/Aerocodex777/gibberlink)

**Key Features Summary:**
- 🔗 Simple and powerful URL shortening
- 📊 Comprehensive analytics
- 🎨 Beautiful, responsive UI
- ⚡ Fast and reliable
- 🔒 Secure and private
- 🌍 Global accessibility
