from flask import Flask, render_template_string, jsonify
from datetime import datetime
import random

app = Flask(__name__)

# HTML Template for Dashboard
DASHBOARD_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Flask Dashboard</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        .header {
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            margin-bottom: 30px;
        }
        h1 {
            color: #333;
            margin-bottom: 10px;
        }
        .timestamp {
            color: #666;
            font-size: 14px;
        }
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .stat-card {
            background: white;
            padding: 25px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            transition: transform 0.3s ease;
        }
        .stat-card:hover {
            transform: translateY(-5px);
        }
        .stat-title {
            color: #666;
            font-size: 14px;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 10px;
        }
        .stat-value {
            color: #333;
            font-size: 32px;
            font-weight: bold;
        }
        .stat-icon {
            font-size: 24px;
            margin-bottom: 10px;
        }
        .chart-container {
            background: white;
            padding: 25px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            margin-bottom: 30px;
        }
        .chart-title {
            color: #333;
            font-size: 18px;
            margin-bottom: 20px;
            font-weight: 600;
        }
        .bar-chart {
            display: flex;
            align-items: flex-end;
            height: 200px;
            gap: 10px;
        }
        .bar {
            flex: 1;
            background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
            border-radius: 5px 5px 0 0;
            position: relative;
            transition: all 0.3s ease;
        }
        .bar:hover {
            opacity: 0.8;
        }
        .bar-label {
            text-align: center;
            margin-top: 10px;
            font-size: 12px;
            color: #666;
        }
        .refresh-btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 12px 30px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
            font-weight: 600;
            transition: transform 0.2s ease;
        }
        .refresh-btn:hover {
            transform: scale(1.05);
        }
        .refresh-btn:active {
            transform: scale(0.95);
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 Dashboard</h1>
            <p class="timestamp" id="timestamp">Loading...</p>
        </div>
        
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-icon">👥</div>
                <div class="stat-title">Total Users</div>
                <div class="stat-value" id="users">0</div>
            </div>
            <div class="stat-card">
                <div class="stat-icon">💰</div>
                <div class="stat-title">Revenue</div>
                <div class="stat-value" id="revenue">$0</div>
            </div>
            <div class="stat-card">
                <div class="stat-icon">📈</div>
                <div class="stat-title">Growth</div>
                <div class="stat-value" id="growth">0%</div>
            </div>
            <div class="stat-card">
                <div class="stat-icon">⭐</div>
                <div class="stat-title">Rating</div>
                <div class="stat-value" id="rating">0.0</div>
            </div>
        </div>
        
        <div class="chart-container">
            <h2 class="chart-title">Weekly Activity</h2>
            <div class="bar-chart" id="barChart"></div>
        </div>
        
        <div style="text-align: center;">
            <button class="refresh-btn" onclick="loadData()">🔄 Refresh Data</button>
        </div>
    </div>
    
    <script>
        function loadData() {
            fetch('/api/stats')
                .then(response => response.json())
                .then(data => {
                    document.getElementById('timestamp').textContent = 'Last updated: ' + data.timestamp;
                    document.getElementById('users').textContent = data.users.toLocaleString();
                    document.getElementById('revenue').textContent = '$' + data.revenue.toLocaleString();
                    document.getElementById('growth').textContent = data.growth + '%';
                    document.getElementById('rating').textContent = data.rating.toFixed(1);
                    
                    // Update chart
                    const chartContainer = document.getElementById('barChart');
                    chartContainer.innerHTML = '';
                    
                    const days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
                    const maxValue = Math.max(...data.weekly_data);
                    
                    data.weekly_data.forEach((value, index) => {
                        const barWrapper = document.createElement('div');
                        barWrapper.style.flex = '1';
                        barWrapper.style.display = 'flex';
                        barWrapper.style.flexDirection = 'column';
                        barWrapper.style.alignItems = 'center';
                        
                        const bar = document.createElement('div');
                        bar.className = 'bar';
                        bar.style.height = (value / maxValue * 100) + '%';
                        bar.title = value + ' visits';
                        
                        const label = document.createElement('div');
                        label.className = 'bar-label';
                        label.textContent = days[index];
                        
                        barWrapper.appendChild(bar);
                        barWrapper.appendChild(label);
                        chartContainer.appendChild(barWrapper);
                    });
                });
        }
        
        // Load data on page load
        loadData();
        
        // Auto-refresh every 30 seconds
        setInterval(loadData, 30000);
    </script>
</body>
</html>
'''

@app.route("/")
def home():
    return render_template_string(DASHBOARD_TEMPLATE)

@app.route("/api/stats")
def get_stats():
    # Generate random data for demonstration
    stats = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "users": random.randint(1000, 5000),
        "revenue": random.randint(10000, 50000),
        "growth": round(random.uniform(5.0, 25.0), 1),
        "rating": round(random.uniform(4.0, 5.0), 1),
        "weekly_data": [random.randint(50, 200) for _ in range(7)]
    }
    return jsonify(stats)

if __name__ == "__main__":
    app.run(debug=True)