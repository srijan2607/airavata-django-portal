# Performance Measurement Guide

**Purpose:** Reproducible performance measurement procedures for Apache Airavata Django Portal
**Created:** 2025-11-09
**Author:** Srijan
**For:** Python 3.12 Migration - Performance Baseline and Regression Detection

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Tool Installation](#tool-installation)
3. [Environment Setup](#environment-setup)
4. [API Performance Measurement](#api-performance-measurement)
5. [Page Load Performance Measurement](#page-load-performance-measurement)
6. [Database Query Analysis](#database-query-analysis)
7. [Memory Profiling](#memory-profiling)
8. [Interpreting Results](#interpreting-results)
9. [Comparing Against Baseline](#comparing-against-baseline)
10. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### System Requirements
- **Operating System:** macOS, Linux, or WSL2 on Windows
- **Python:** 3.6+ (baseline) or 3.12+ (target)
- **Database:** PostgreSQL 12+ (production) or SQLite (development)
- **Memory:** Minimum 4GB RAM available
- **Disk:** 1GB free space for test data and logs

### Required Access
- Development environment with all dependencies installed
- Database with representative test data
- Admin/superuser account for Debug Toolbar access

---

## Tool Installation

### 1. Apache Bench (ab)

**macOS:**
```bash
# Apache Bench comes with Apache HTTP Server
brew install httpd

# Verify installation
ab -V
# Expected output: ApacheBench, Version 2.3
```

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install apache2-utils

# Verify
ab -V
```

**Verification:**
```bash
$ ab -V
This is ApacheBench, Version 2.3 <$Revision: 1913912 $>
Copyright 1996 Adam Twiss, Zeus Technology Ltd
```

### 2. curl Timing Format File

Create `curl-format.txt` in project root:

```bash
cat > curl-format.txt << 'EOF'
    time_namelookup:  %{time_namelookup}s\n
       time_connect:  %{time_connect}s\n
    time_appconnect:  %{time_appconnect}s\n
   time_pretransfer:  %{time_pretransfer}s\n
      time_redirect:  %{time_redirect}s\n
 time_starttransfer:  %{time_starttransfer}s\n
                    ----------\n
         time_total:  %{time_total}s\n
EOF
```

**Verify:**
```bash
curl -w "@curl-format.txt" -o /dev/null -s http://example.com
```

### 3. Django Debug Toolbar

```bash
# Install compatible version for Django 3.2
pip install 'django-debug-toolbar<4.0'

# For Django 4.2+
pip install django-debug-toolbar
```

**Configuration already added to:**
- `django_airavata/settings.py` - INSTALLED_APPS and MIDDLEWARE
- `django_airavata/urls.py` - Debug Toolbar URLs

### 4. Optional: Lighthouse CLI

```bash
# Install Node.js first if not available
npm install -g lighthouse

# Verify
lighthouse --version
```

---

## Environment Setup

### 1. Start Development Server

```bash
# Ensure you're in project root
cd /path/to/airavata-django-portal

# Activate virtual environment
source venv/bin/activate

# Run migrations if needed
python manage.py migrate

# Start server
python manage.py runserver
```

**Verify server is running:**
```bash
curl -I http://localhost:8000/
# Should return HTTP 200 or 302 (redirect)
```

### 2. Enable Debug Mode

In `django_airavata/settings.py`:
```python
DEBUG = True
INTERNAL_IPS = ['127.0.0.1']
```

### 3. Prepare Test Data

**Create test projects:**
```bash
python manage.py shell
```

```python
from django_airavata.apps.workspace.models import Project
from django.contrib.auth import get_user_model

User = get_user_model()
user = User.objects.first()  # or create test user

# Create 10 test projects
for i in range(10):
    Project.objects.create(
        name=f"Test Project {i}",
        owner=user,
        description=f"Performance baseline test project {i}"
    )
```

### 4. Authenticate for API Testing

**Get authentication token or session:**
```bash
# Login via browser first
open http://localhost:8000/auth/login/

# Or use Django shell to create session
python manage.py createsuperuser  # if needed
```

---

## API Performance Measurement

### Critical Endpoints to Measure

1. `/api/projects/` - Workspace projects list
2. `/api/experiments/` - Experiments list
3. `/api/applications/` - Application catalog
4. `/api/user-profiles/` - User profile (if authenticated)

### Measurement Procedure

**1. Projects API:**
```bash
ab -n 1000 -c 10 -g performance-projects.tsv \
   http://localhost:8000/api/projects/
```

**Parameters:**
- `-n 1000` - Total requests
- `-c 10` - Concurrent requests (simulates 10 users)
- `-g performance-projects.tsv` - Graph data output

**Output to capture:**
```
Requests per second:    [X] #/sec (mean)
Time per request:       [Y] ms (mean)
Time per request:       [Z] ms (mean, across all concurrent requests)

Percentage of requests served within certain time (ms)
  50%    [median]
  66%    [...]
  75%    [...]
  80%    [...]
  90%    [...]
  95%    [p95]
  98%    [...]
  99%    [p99]
 100%    [longest request]
```

**2. Experiments API:**
```bash
ab -n 1000 -c 10 -g performance-experiments.tsv \
   http://localhost:8000/api/experiments/
```

**3. Applications API:**
```bash
ab -n 1000 -c 10 -g performance-applications.tsv \
   http://localhost:8000/api/applications/
```

### With Authentication

If endpoints require authentication:

```bash
# Get session cookie from browser DevTools
# Network tab -> Copy cookie header

ab -n 1000 -c 10 \
   -H "Cookie: sessionid=YOUR_SESSION_ID" \
   http://localhost:8000/api/projects/
```

### Detailed Timing with curl

```bash
curl -w "@curl-format.txt" -o /dev/null -s \
     http://localhost:8000/api/projects/
```

**Example output:**
```
    time_namelookup:  0.002s
       time_connect:  0.003s
    time_appconnect:  0.000s
   time_pretransfer:  0.003s
      time_redirect:  0.000s
 time_starttransfer:  0.156s (TTFB - Time To First Byte)
                    ----------
         time_total:  0.158s (Total time)
```

---

## Page Load Performance Measurement

### 1. Homepage Load Time

```bash
curl -w "@curl-format.txt" -o /dev/null -s http://localhost:8000/
```

**Record:**
- `time_starttransfer` = TTFB (Time to First Byte)
- `time_total` = Full page load (server-side)

### 2. Workspace Dashboard

```bash
curl -w "@curl-format.txt" -o /dev/null -s \
     -H "Cookie: sessionid=YOUR_SESSION_ID" \
     http://localhost:8000/workspace/dashboard/
```

### 3. Browser-Based Measurements (Chrome DevTools)

**Steps:**
1. Open Chrome DevTools (F12 or Cmd+Option+I)
2. Navigate to Network tab
3. Check "Disable cache"
4. Hard reload page (Cmd+Shift+R / Ctrl+Shift+R)

**Metrics to record:**
- **DOMContentLoaded:** Blue line in timeline (DOM ready)
- **Load:** Red line in timeline (all resources loaded)
- **Finish:** Total time to complete all requests

**Performance tab metrics:**
- **First Paint (FP):** First pixel rendered
- **First Contentful Paint (FCP):** First text/image rendered
- **Largest Contentful Paint (LCP):** Largest element visible
- **Time to Interactive (TTI):** Page becomes interactive

### 4. Lighthouse Audit (Optional)

```bash
lighthouse http://localhost:8000/ \
  --output json \
  --output-path ./docs/lighthouse-baseline.json \
  --only-categories=performance \
  --chrome-flags="--headless"
```

**Key metrics from Lighthouse:**
- Performance Score (0-100)
- First Contentful Paint
- Largest Contentful Paint
- Total Blocking Time
- Cumulative Layout Shift
- Speed Index

---

## Database Query Analysis

### 1. Enable Query Logging

Already configured in `django_airavata/settings.py`:
```python
LOGGING = {
    'loggers': {
        'django.db.backends': {
            'handlers': ['console', 'console_debug'],
            'level': 'DEBUG' if DEBUG else 'INFO',
            'propagate': False,
        }
    }
}
```

### 2. Run Server with Query Logging

```bash
python manage.py runserver 2>&1 | tee server-queries.log
```

### 3. Access Endpoints and Capture Queries

```bash
# In another terminal
curl http://localhost:8000/api/projects/
curl http://localhost:8000/workspace/dashboard/
curl http://localhost:8000/api/experiments/
```

### 4. Analyze Logged Queries

```bash
# Extract SQL queries
grep "SELECT" server-queries.log > queries.log

# Find slowest queries (if execution time logged)
grep "SELECT" server-queries.log | \
  grep -o '[0-9.]*s$' | \
  sort -rn | \
  head -10
```

### 5. Use Django Debug Toolbar

**Steps:**
1. Access endpoint in browser: `http://localhost:8000/api/projects/`
2. Look for Debug Toolbar on right side of page
3. Click "SQL" panel

**Metrics to record:**
- Total number of queries
- Total query execution time
- Duplicate queries (N+1 issues)
- Slowest individual queries

**Identify N+1 Queries:**
- Look for repeated similar queries with different IDs
- Example:
  ```
  SELECT * FROM experiments WHERE id = 1  (0.5ms)
  SELECT * FROM experiments WHERE id = 2  (0.5ms)
  SELECT * FROM experiments WHERE id = 3  (0.5ms)
  ... (Repeated many times = N+1 problem)
  ```

### 6. Document Top 10 Slowest Queries

For each slow query, record:
```json
{
  "query": "SELECT * FROM workspace_experiment WHERE user_id = 123",
  "execution_time_ms": 450,
  "frequency": "high",
  "endpoint": "/api/experiments/",
  "optimization_potential": "Add index on user_id"
}
```

---

## Memory Profiling

### 1. Baseline Idle Memory

```bash
# Start server
python manage.py runserver &
SERVER_PID=$!

# Wait for server to fully start
sleep 5

# Measure memory
ps -p $SERVER_PID -o rss,vsz,pmem,comm
```

**Output columns:**
- `RSS` - Resident Set Size (actual RAM used)
- `VSZ` - Virtual Size (total memory allocated)
- `%MEM` - Percentage of total system memory

### 2. Memory Under Load

**Terminal 1 - Monitor memory:**
```bash
# Continuous monitoring
watch -n 1 'ps aux | grep "[p]ython.*manage.py runserver"'
```

**Terminal 2 - Generate load:**
```bash
# Sustained load test (10 minutes)
ab -n 10000 -c 50 -t 600 http://localhost:8000/api/projects/
```

**Record:**
- Initial memory (RSS) in MB
- Peak memory during load
- Final memory after load
- Memory growth over time (indicates potential leak)

### 3. Memory Leak Detection

**Criteria:**
- ✅ **No leak:** Memory stabilizes after load stops
- ⚠️ **Potential leak:** Memory continues growing gradually
- 🚨 **Definite leak:** Memory grows continuously, never stabilizes

**Long-running test:**
```bash
# 1 hour sustained load
ab -n 100000 -c 20 -t 3600 http://localhost:8000/ &

# Monitor memory every 5 minutes
for i in {1..12}; do
  date
  ps aux | grep "[p]ython.*manage.py runserver" | awk '{print $6, $11}'
  sleep 300  # 5 minutes
done
```

### 4. Python-Specific Memory Profiling (Advanced)

```bash
pip install memory-profiler psutil

# Profile specific view
python -m memory_profiler manage.py shell
```

```python
from memory_profiler import profile

@profile
def test_endpoint():
    import requests
    for i in range(100):
        requests.get('http://localhost:8000/api/projects/')

test_endpoint()
```

---

## Interpreting Results

### API Performance

**Good Performance:**
- Mean response time: < 200ms
- p95: < 500ms
- p99: < 1000ms
- Requests per second: > 50 RPS

**Performance Issues:**
- Mean > 500ms: Database queries need optimization
- p95 > 2000ms: Timeout risk, investigate slow queries
- Failed requests > 0: Application errors, check logs

### Page Load Performance

**Good Performance:**
- TTFB: < 200ms
- Full Load: < 2 seconds
- LCP: < 2.5 seconds

**Performance Issues:**
- TTFB > 500ms: Server-side rendering slow
- Full Load > 5s: Too many resources or slow queries
- LCP > 4s: Largest element loads too late

### Database Queries

**Healthy Patterns:**
- < 20 queries per API request
- No duplicate queries
- All queries < 100ms

**Issues:**
- > 50 queries per request: N+1 problem
- Queries > 500ms: Missing indexes
- Duplicate queries: Need select_related() or prefetch_related()

### Memory

**Normal Behavior:**
- Idle: 200-400MB RSS
- Under load: 400-800MB RSS
- Growth: Stabilizes after load stops

**Memory Issues:**
- Idle > 1GB: Potential memory leak
- Growth > 50% during load: Investigate caching
- Never stabilizes: Definite memory leak

---

## Comparing Against Baseline

### 1. Load Baseline Metrics

```bash
cat docs/performance-baseline.json
```

### 2. Calculate Differences

**API Response Time:**
```
Increase % = ((New Mean - Baseline Mean) / Baseline Mean) * 100

Example:
Baseline: 150ms
New: 165ms
Increase % = ((165 - 150) / 150) * 100 = 10%
```

**Threshold Check:**
```
✅ < 10% increase: Acceptable
⚠️ 10-20% increase: Review needed
🚨 > 20% increase: Regression detected
```

### 3. Regression Decision Matrix

| Metric | Threshold | Action |
|--------|-----------|--------|
| API Mean | +10% | Investigate if exceeded |
| API p95 | +15% | Review query performance |
| Page Load | +15% | Check static assets |
| Memory | +20% | Profile memory usage |
| Query Count | +25% | Review ORM usage |

### 4. Automated Comparison Script

```python
import json

def compare_performance(baseline_file, new_file):
    with open(baseline_file) as f:
        baseline = json.load(f)
    with open(new_file) as f:
        new = json.load(f)

    regressions = []

    # Compare API metrics
    for endpoint in baseline['api_performance']:
        base_mean = baseline['api_performance'][endpoint]['mean_ms']
        new_mean = new['api_performance'][endpoint]['mean_ms']

        if base_mean and new_mean:
            increase = ((new_mean - base_mean) / base_mean) * 100

            if increase > 10:
                regressions.append({
                    'endpoint': endpoint,
                    'baseline': base_mean,
                    'new': new_mean,
                    'increase_pct': increase
                })

    return regressions

# Usage
regressions = compare_performance(
    'docs/performance-baseline.json',
    'docs/performance-phase2.json'
)

for r in regressions:
    print(f"⚠️ {r['endpoint']}: {r['baseline']}ms -> {r['new']}ms (+{r['increase_pct']:.1f}%)")
```

---

## Troubleshooting

### Issue: Apache Bench Connection Refused

**Symptoms:**
```
ab: apr_socket_recv: Connection refused (61)
```

**Solutions:**
1. Verify server is running: `curl -I http://localhost:8000/`
2. Check port: Server might be on different port (e.g., 8001)
3. Firewall: Ensure localhost connections allowed

### Issue: High Failed Request Count

**Symptoms:**
```
Failed requests:        250
```

**Solutions:**
1. Check server logs for errors
2. Increase timeout: `ab -s 30 ...` (30 second timeout)
3. Reduce concurrency: `-c 5` instead of `-c 10`

### Issue: Debug Toolbar Not Showing

**Solutions:**
1. Verify DEBUG=True in settings
2. Check INTERNAL_IPS includes '127.0.0.1'
3. Ensure middleware is added
4. Access page in browser (not curl)

### Issue: Memory Measurements Vary Widely

**Solutions:**
1. Run server in fresh environment
2. Clear caches before measurement
3. Take multiple measurements and average
4. Ensure no other processes using memory

### Issue: grpcio Installation Fails

**Symptoms:**
```
error: command '/usr/bin/clang++' failed with exit code 1
```

**Solutions:**
1. Use Python 3.6-3.10 for baseline measurements
2. OR upgrade grpcio to 1.60+ for Python 3.12 compatibility
3. Document issue and defer actual measurements

---

## Next Steps After Baseline

1. **Store Baseline:**
   - Commit `performance-baseline.json` to git
   - Tag commit: `git tag performance-baseline-phase1`

2. **Schedule Re-Measurements:**
   - After Django 4.2 upgrade (Phase 2)
   - After Wagtail 7.0 upgrade (Phase 3)
   - After dependency updates (Phase 4)
   - After Python 3.12 runtime deployment (Phase 5)

3. **Automated Testing:**
   - Integrate performance tests into CI/CD
   - Set up performance monitoring (New Relic, DataDog)
   - Create alerts for regression thresholds

4. **Documentation:**
   - Update this guide with actual baseline values once measured
   - Document any environment-specific quirks
   - Share measurement procedures with team

---

**Created:** 2025-11-09
**Last Updated:** 2025-11-09
**Version:** 1.0
**Author:** Srijan
