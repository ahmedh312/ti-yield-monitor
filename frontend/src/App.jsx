import React, { useEffect, useState } from 'react';
import { 
  PieChart, Pie, Cell, Tooltip, ResponsiveContainer, 
  LineChart, Line, XAxis, YAxis, CartesianGrid 
} from 'recharts';

const App = () => {
  const [data, setData] = useState({ 
    counts: { PASS: 0, FAIL: 0 }, 
    trend: [] 
  });

  // Safety Check: Calculate totals only if data.counts exists
  const passCount = data?.counts?.PASS || 0;
  const failCount = data?.counts?.FAIL || 0;
  const total = passCount + failCount;
  const yieldRate = total > 0 ? ((passCount / total) * 100).toFixed(1) : "0.0";

  useEffect(() => {
    const updateDashboard = () => {
      fetch('http://127.0.0.1:5000/api/stats')
        .then(res => res.json())
        .then(json => {
            if(json) setData(json);
        })
        .catch(err => console.error("API Error:", err));
    };

    updateDashboard();
    const interval = setInterval(updateDashboard, 3000);
    return () => clearInterval(interval);
  }, []);

  const handleReset = () => {
    if (window.confirm("Reset all factory data?")) {
      fetch('http://127.0.0.1:5000/api/reset', { method: 'POST' })
        .then(() => setData({ counts: { PASS: 0, FAIL: 0 }, trend: [] }))
        .catch(err => console.error("Reset failed:", err));
    }
  };

  const chartData = [
    { name: 'Pass', value: passCount },
    { name: 'Fail', value: failCount },
  ];

  const handleExport = () => {
  // Opening the API URL in a new window triggers a file download automatically
  window.open('http://127.0.0.1:5000/api/export', '_blank');
  };

  const statusColor = parseFloat(yieldRate) >= 90 ? '#00C49F' : '#FF4444';

  return (
    <div style={{ minHeight: '100vh', backgroundColor: '#121212', color: '#fff', padding: '40px', fontFamily: 'Arial' }}>
      <div style={{ maxWidth: '1200px', margin: '0 auto' }}>
        
        <header style={{ display: 'flex', justifyContent: 'space-between', borderBottom: '1px solid #333', paddingBottom: '20px', marginBottom: '30px' }}>
          <h1 style={{ margin: 0 }}>TI FAB MONITOR</h1>
          <button onClick={handleReset} style={{ cursor: 'pointer', color: '#CC0000', border: '1px solid #CC0000', background: 'none', padding: '5px 15px' }}>RESET</button>
        </header>

        <header style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderBottom: '2px solid #CC0000', paddingBottom: '15px', marginBottom: '25px' }}>
          <h1 style={{ margin: 0, fontSize: '24px' }}>TI FAB 21 | OPERATIONAL MONITOR</h1>
          <div style={{ display: 'flex', gap: '10px' }}>
            <button onClick={handleExport} style={{ background: '#CC0000', border: 'none', color: '#fff', cursor: 'pointer', padding: '8px 16px', borderRadius: '4px', fontWeight: 'bold' }}>
              GENERATE SHIFT REPORT
            </button>
            <button onClick={handleReset} style={{ background: 'transparent', border: '1px solid #CC0000', color: '#CC0000', cursor: 'pointer', padding: '8px 16px', borderRadius: '4px' }}>
              RESET
            </button>
          </div>
      </header>

        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '30px' }}>
          
          {/* STATS SECTION */}
          <div>
            <div style={{ background: '#1a1a1a', padding: '30px', borderRadius: '15px', borderLeft: `10px solid ${statusColor}`, marginBottom: '20px' }}>
              <h2 style={{ fontSize: '14px', color: '#888', margin: 0 }}>CURRENT YIELD</h2>
              <div style={{ fontSize: '64px', fontWeight: 'bold' }}>{yieldRate}%</div>
              <p>Total Wafers: {total}</p>
            </div>

            {/* TREND LINE */}
            <div style={{ background: '#1a1a1a', padding: '20px', borderRadius: '15px', height: '300px' }}>
              <h3 style={{ fontSize: '12px', color: '#888' }}>YIELD TREND</h3>
              <ResponsiveContainer width="100%" height="90%">
                <LineChart data={data.trend || []}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#333" />
                  <XAxis dataKey="time" stroke="#666" fontSize={10} interval={0} tick={{ angle: -35, textAnchor: 'end' }} height={50} />
                  <YAxis domain={[0, 100]} stroke="#666" tickFormatter={(value) => `${value}%`}/>
                  <Tooltip contentStyle={{backgroundColor: '#222', border: 'none'}} />
                  <Line type="monotone" dataKey="yield" stroke="#CC0000" strokeWidth={3} dot={{ r: 5 }} />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* PIE CHART SECTION */}
          <div style={{ background: '#1a1a1a', padding: '30px', borderRadius: '15px', display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
            <h3 style={{ alignSelf: 'flex-start', fontSize: '12px', color: '#888' }}>DISTRIBUTION</h3>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie data={chartData} innerRadius={80} outerRadius={100} dataKey="value" stroke="none">
                  <Cell fill="#00C49F" />
                  <Cell fill="#FF4444" />
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </div>

        </div>
      </div>
    </div>
  );
};

export default App;