# CloudSpend — FinOps Monitoring Engine

**A multi-cloud cost optimization and idle resource detection system for AWS, GCP, and Azure**

![Status](https://img.shields.io/badge/status-active-brightgreen) ![Python](https://img.shields.io/badge/Python-3.9+-blue) ![React](https://img.shields.io/badge/React-18+-blue) ![MongoDB](https://img.shields.io/badge/MongoDB-Atlas-green)

---

## Overview

CloudSpend is a **FinOps (Financial Operations) monitoring engine** that automatically detects idle cloud resources across AWS, GCP, and Azure, triggers cost-saving actions, and provides real-time visibility into multi-cloud spending patterns.

**Why CloudSpend?**
- **Automatic Cost Optimization:** Detects and shuts down idle instances across AWS (EC2), GCP (Compute Engine), and Azure (VMs) → saves ~$7.50/day per idle instance
- **Multi-Cloud Support:** Unified monitoring and cost tracking across AWS, GCP, and Azure with cloud provider identification
- **Multi-Metric Intelligence:** Analyzes CPU, network, and disk utilization simultaneously
- **Real-Time Dashboard:** Live charts showing savings, shutdowns, and cost trends with cloud provider breakdown
- **Business-Focused:** Built for Product Managers, Finance Teams, and DevOps Engineers managing multi-cloud infrastructure

---

## Key Features

### 🔍 **Intelligent Idle Detection**
- **Multi-metric validation:** CPU + Network + Disk all near-zero = IDLE
- **Configurable thresholds** (default: CPU <10%, Network <5MB, Disk <5MB)
- **Automated shutdown** of idle instances to freeze billing

### 💰 **Cost Tracking & Analytics**
- **Real-time savings calculation** ($0.0104/hour per idle instance)
- **Daily/Monthly/Yearly trends** visualized on dashboard
- **Cumulative savings** across all scans

### 🚀 **Automated Actions**
- **Background scheduler** runs policy engine every 5 minutes
- **Auto-shutdown idle instances** with billing impact calculation
- **Detailed logging** of all decisions and actions

### 📊 **Business Intelligence Dashboard**
- Total savings (all-time cumulative across all clouds)
- Active vs. Idle instance breakdown by cloud provider
- Hourly/Daily/Monthly cost trends with multi-cloud analysis
- Instance status table with CPU, network, disk metrics, and cloud provider identification
- Color-coded cloud provider indicators (AWS, GCP, Azure) for quick visual reference

---

## Dashboard Screenshots

   ![Dashboard Overview](screenshots/dashboard1.png)
*Figure 1: CloudSpend dashboard showing multi-cloud instance monitoring with color-coded cloud provider indicators*

   ![Dashboard Overview](screenshots/dashboard2.png)
*Figure 2: Real-time savings metrics and active vs. idle instance breakdown across AWS, GCP, and Azure*

---

## Architecture

```
┌─────────────────────────────────────────┐
│         React Frontend (Port 3000)      │
│  - Dashboard with live charts            │
│  - Real-time savings metrics             │
│  - Multi-cloud instance monitoring       │
│  - Cloud provider identification         │
└────────────────┬────────────────────────┘
                 │ REST API (JSON)
┌────────────────▼────────────────────────┐
│      Flask Backend (Port 5000)          │
│  - /api/results → All scan results      │
│  - /api/summary → Cost aggregation      │
│  - /api/daily/monthly/yearly → Trends   │
└────────────────┬───────────────┬────────┘
                 │               │ PyMongo Driver
    ┌────────────▼──────────┐    │
    │  Cloud Adapter Layer  │    │
    ├──────────────────────┤    │
    │  ├─ AWSAdapter       │    │
    │  │  (EC2 + moto)    │    │
    │  ├─ GCPAdapter       │    │
    │  │  (Compute mock)   │    │
    │  └─ AzureAdapter     │    │
    │     (VMs mock)       │    │
    └────────────┬─────────┘    │
                 │              │
┌────────────────▼──────────────▼─────────┐
│    MongoDB Atlas (Cloud Database)        │
│  - scans collection: Multi-cloud results│
│  - cloud_provider field per instance    │
│  - Persistent storage across deploys    │
└─────────────────────────────────────────┘

Background Scheduler (Every 5 min)
  ↓
Policy Engine (Multi-Cloud Adapter)
  ├─ Fetch instances from AWS (EC2)
  ├─ Fetch instances from GCP (Compute)
  ├─ Fetch instances from Azure (VMs)
  ├─ Analyze metrics (CPU, Network, Disk)
  ├─ Detect idle resources across all clouds
  ├─ Auto-shutdown with cloud provider tracking
  └─ Store results in MongoDB with cloud tags
```

---

## Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Frontend** | React 18, Recharts, Tailwind CSS | Interactive dashboard with live multi-cloud charts |
| **Backend** | Flask, Flask-CORS | REST API for data retrieval |
| **Database** | MongoDB Atlas | Scan results & historical multi-cloud data |
| **Cloud Adapters** | Python abstract base class pattern | Unified interface for AWS, GCP, Azure integrations |
| **Cloud Mocking** | Boto3, Moto (AWS); Mock (GCP/Azure) | EC2, Compute Engine, Azure VM APIs (mocked for dev) |
| **Scheduling** | APScheduler | Background policy engine (every 5 min, all clouds) |
| **Environment** | Python 3.9+, Node.js 18+ | Runtime dependencies |

---

## Installation & Setup

### Prerequisites
- Python 3.9+
- Node.js 18+
- MongoDB Atlas account (free tier OK)
- Git

### Backend Setup

```bash
# Clone repository
git clone https://github.com/Jothika2506/CloudSpend.git
cd CloudSpend

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r backend/requirements.txt

# Configure environment
# Create .env file in root:
MONGODB_URI="mongodb+srv://username:password@cluster.xxxxx.mongodb.net/cloudspend?retryWrites=true&w=majority"
LOAD_MOCK_DATA=true  # Set to 'false' for production with real AWS

# Start backend
cd backend
python app.py
```

**Backend runs on:** `http://localhost:5000`

### Frontend Setup

```bash
# In new terminal, from root directory
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

**Frontend runs on:** `http://localhost:3000`

---

## Usage

### Development Mode (with Mock Data)

```bash
# Backend with mock data
LOAD_MOCK_DATA=true python backend/app.py

# Frontend (separate terminal)
cd frontend && npm start
```

**What happens:**
1. ✅ Backend connects to MongoDB Atlas
2. ✅ Mock multi-cloud environment loads (AWS EC2, GCP Compute, Azure VMs with randomized instances)
3. ✅ Policy engine runs immediately across all three clouds (detects idle instances)
4. ✅ Results stored in MongoDB with cloud provider tags
5. ✅ Dashboard populates with multi-cloud charts & metrics with color-coded provider identification

### API Endpoints

```bash
# Get all scan results
GET http://localhost:5000/api/results

# Get latest scan only
GET http://localhost:5000/api/latest

# Get summary statistics
GET http://localhost:5000/api/summary
# Response:
{
  "total_runs": 12,
  "total_hourly_saving": 0.0416,
  "total_idle_detected": 48,
  "avg_saving_per_run": 0.0035,
  "latest_timestamp": "2026-09-07 16:38:23",
  "clouds": {
    "AWS": {"total_instances": 24, "idle_instances": 12},
    "GCP": {"total_instances": 18, "idle_instances": 8},
    "Azure": {"total_instances": 20, "idle_instances": 10}
  }
}

# Get daily/monthly/yearly trends
GET http://localhost:5000/api/daily
GET http://localhost:5000/api/monthly
GET http://localhost:5000/api/yearly
```

---

## Project Structure

```
CloudSpend/
├── backend/
│   ├── app.py                    # Flask server + API routes + scheduler
│   ├── requirements.txt          # Python dependencies
│   ├── models/                   # Data models (future use)
│   ├── adapters/                 # Cloud provider adapters (multi-cloud pattern)
│   │   ├── __init__.py           # Exports all adapter classes
│   │   ├── cloud_adapter.py      # Abstract base class (CloudAdapter)
│   │   ├── aws_adapter.py        # AWS EC2 implementation (AWSAdapter)
│   │   ├── gcp_adapter.py        # GCP Compute implementation (GCPAdapter)
│   │   └── azure_adapter.py      # Azure VM implementation (AzureAdapter)
│   ├── scripts/
│   │   ├── policy_engine.py      # Core FinOps idle detection logic (multi-cloud)
│   │   └── mock_setup.py         # Mock cloud environments
│   └── data/
│       └── results.json          # Local data backup
├── frontend/
│   ├── src/
│   │   ├── App.js                # Main React app — dashboard UI (multi-cloud)
│   │   ├── App.css               # Component styles
│   │   └── index.js              # React entry point
│   ├── public/
│   └── package.json
├── venv/                         # Python virtual environment
├── .env                          # Environment variables (gitignored)
├── .gitignore
└── README.md
```

---

## How It Works

### 1️⃣ **Scan Phase** (Every 5 minutes)
```
Policy Engine starts
  ↓
Cloud Adapter Layer initializes (AWS, GCP, Azure)
  ├─ Fetch EC2 instances from AWS → tag with cloud_provider: "AWS"
  ├─ Fetch Compute instances from GCP → tag with cloud_provider: "GCP"
  └─ Fetch VMs from Azure → tag with cloud_provider: "Azure"
  ↓
Get metrics for all instances (CPU, Network, Disk)
  ↓
Apply idle detection logic across all clouds
```

### 2️⃣ **Analysis Phase**
```
For each instance:
  IF cpu < 10% AND network < 5MB AND disk < 5MB:
    → IDLE
    → Calculate saving: $0.0104/hour
  ELSE:
    → ACTIVE
    → Keep running
```

### 3️⃣ **Action Phase**
```
IF idle instances found:
  → Shut down instance (freeze billing)
  → Log action + timestamp + cloud provider
  ↓
Store result in MongoDB
  ├─ Timestamp
  ├─ Total instances scanned per cloud
  ├─ Idle/Active count per cloud
  ├─ Hourly saving aggregated & per cloud
  ├─ Cloud provider identification (AWS/GCP/Azure)
  └─ Detailed instance breakdown with cloud tags
```

### 4️⃣ **Dashboard Phase**
```
Frontend fetches /api/results
  ↓
Aggregates data by day/month/year with multi-cloud breakdown
  ↓
Displays charts:
  - Total saved (cumulative across all clouds)
  - Active vs Idle pie chart (all clouds combined)
  - Savings trend line chart (multi-cloud)
  - Instance status table with cloud provider column
    └─ Color-coded indicators: AWS (#FF9900), GCP (#4285F4), Azure (#0078D4)
```

---

## Live Scan Output

![Scheduler Output](scheduler-output.png)
*Figure 3: Multi-cloud scan output from APScheduler showing instances detected across AWS, GCP, and Azure with real-time metrics and idle detection*

---

## Configuration

### Environment Variables (`.env`)

```dotenv
# MongoDB Connection (REQUIRED)
MONGODB_URI=mongodb+srv://username:password@cluster.xxxxx.mongodb.net/database

# Load mock data on startup (for development — mocks all three clouds)
LOAD_MOCK_DATA=true

# For production multi-cloud connection:
# AWS credentials
# AWS_ACCESS_KEY_ID=xxx
# AWS_SECRET_ACCESS_KEY=xxx
# AWS_REGION=us-east-1

# GCP credentials
# GOOGLE_APPLICATION_CREDENTIALS=/path/to/gcp-key.json
# GCP_PROJECT_ID=your-project-id

# Azure credentials
# AZURE_SUBSCRIPTION_ID=xxx
# AZURE_CLIENT_ID=xxx
# AZURE_CLIENT_SECRET=xxx
# AZURE_TENANT_ID=xxx
```

### Policy Engine Thresholds

Edit `backend/scripts/policy_engine.py`:

```python
CPU_THRESHOLD = 10.0          # % CPU utilization
NETWORK_THRESHOLD = 5.0       # MB/s network traffic
DISK_THRESHOLD = 5.0          # MB/s disk I/O
```

---

## Dashboard Metrics Explained

| Metric | Meaning | Formula |
|--------|---------|---------|
| **Total Saved** | Cumulative savings across all scans | sum(hourly_saving * hours_since_shutdown) |
| **Total Shutdowns** | Number of idle instances shut down | count(idle_count) |
| **Current Waste %** | % of resources sitting idle now | idle_count / total_instances * 100 |
| **Monthly Projection** | Estimated monthly savings if pattern continues | avg_saving_per_run * runs_per_month |
| **Active vs Idle** | Instance utilization breakdown | pie chart of status counts |

---

## Development Roadmap

**Completed:**
- ✅ Multi-metric idle detection (CPU + Network + Disk)
- ✅ Real-time dashboard with charts
- ✅ MongoDB integration for persistent storage
- ✅ Background scheduler (every 5 min)
- ✅ RESTful API for data retrieval
- ✅ **Multi-Cloud Support** — AWS, GCP, and Azure adapter architecture with cloud provider identification

**Planned for Future:**
- [ ] **Snapshot before shutdown** — EC2 snapshot creation before instance termination
- [ ] **Cost attribution** — Map savings back to specific teams/projects across clouds
- [ ] **Real Cloud Integration** — Connect to actual AWS, GCP, and Azure accounts (replace mocks)
- [ ] **Budget Alerts** — Email/Slack notifications when spending exceeds threshold
- [ ] **Regional Breakdown** — Cost analysis by region per cloud provider
- [ ] **Instance Tagging** — Exclude production/critical instances from auto-shutdown
- [ ] **Webhook Integration** — Send alerts to external monitoring tools
- [ ] **Audit Logs** — Track who authorized each shutdown action
- [ ] **Multi-Account Support** — Monitor across multiple accounts per cloud provider
- [ ] **Cloud Cost Comparison** — Analyze cost optimization opportunities across clouds

---

## Common Issues

### Issue: "No connection could be made to localhost:27017"
**Fix:** Ensure `MONGODB_URI` is set in `.env` and MongoDB Atlas has whitelisted your IP.

```bash
# Check .env is correct:
cat .env

# Whitelist IP in MongoDB Atlas:
# Settings → Network Access → Add IP Address
```

### Issue: Frontend shows "NaN%" or $0 in metrics
**Fix:** Backend has no data. Mock data is generated automatically by the scheduler when `app.py` runs. Ensure `MONGODB_URI` is set correctly in `.env` and restart the backend.

### Issue: Policy engine not running in background
**Fix:** Ensure APScheduler started. Check for errors in backend logs.

---

## Testing

### Manual API Testing
```bash
# Terminal 1: Start backend
cd backend && python app.py

# Terminal 2: Test endpoints
curl http://localhost:5000/api/summary
curl http://localhost:5000/api/results | python -m json.tool
```

### Mock Data
Mock data is generated automatically by the scheduler every 5 minutes when `app.py` runs. The policy engine creates new scan results with randomized instance data.

To start fresh:
- Stop backend (CTRL+C)
- Clear MongoDB collection in Atlas: `db.scans.deleteMany({})`
- Restart backend: `python app.py`
- Scheduler will generate new scan within 5 minutes
- Refresh dashboard at `http://localhost:3000`

---

## Deployment

### Deploy to Production

```bash
# Build React for production
cd frontend
npm run build

# This creates optimized build/ folder ready for deployment

# Backend: Use production WSGI server (Gunicorn)
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 backend.app:app
```

### Environment Variables for Production (Multi-Cloud)
```dotenv
MONGODB_URI=mongodb+srv://prod-user:secure-password@prod-cluster.mongodb.net/cloudspend
LOAD_MOCK_DATA=false

# AWS credentials
AWS_ACCESS_KEY_ID=your-real-aws-key
AWS_SECRET_ACCESS_KEY=your-real-aws-secret
AWS_REGION=us-east-1

# GCP credentials
GOOGLE_APPLICATION_CREDENTIALS=/secure/gcp-service-account-key.json
GCP_PROJECT_ID=your-gcp-project

# Azure credentials
AZURE_SUBSCRIPTION_ID=your-subscription-id
AZURE_CLIENT_ID=your-client-id
AZURE_CLIENT_SECRET=your-client-secret
AZURE_TENANT_ID=your-tenant-id
```

---

## Performance & Scalability

| Metric | Value | Notes |
|--------|-------|-------|
| **Scan Frequency** | Every 5 min | Configurable via APScheduler, covers all three clouds |
| **Instances per Scan** | 6–21 instances | Randomized mock environment (2–7 per cloud: AWS, GCP, Azure) |
| **API Response Time** | <200ms | MongoDB queries for fast multi-cloud data retrieval |
| **Database Storage** | ~2–3KB per scan | Efficient document-based storage with cloud_provider tags |
| **Cost to Run** | Free | MongoDB Atlas free tier + cloud provider moto mocks (no charges) |
| **Multi-Cloud Support** | AWS, GCP, Azure | Unified adapter pattern for seamless cloud integration |

---

## Contributing

Found a bug? Want to add a feature?

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/awesome-feature`
3. Commit changes: `git commit -m 'Add awesome feature'`
4. Push: `git push origin feature/awesome-feature`
5. Open a Pull Request

---

## License

MIT License — feel free to use for personal & commercial projects.

---

## Contact & Support

- **GitHub:** [Jothika2506/CloudSpend](https://github.com/Jothika2506/CloudSpend)
- **Issues:** Report bugs on GitHub Issues tab
- **Questions:** Open a Discussion

---

## Acknowledgments

Built with:
- **Flask** — Lightweight Python web framework
- **React** — Interactive UI library
- **MongoDB** — Flexible cloud database
- **Boto3** — AWS SDK for Python
- **Moto** — Mock AWS services for testing
- **Cloud Adapter Pattern** — Unified multi-cloud architecture supporting AWS, GCP, and Azure

---

**Made with ☕ for FinOps Engineers & Cloud Cost Optimizers**

Last Updated: October 2026