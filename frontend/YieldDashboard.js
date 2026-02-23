import React, { useEffect, useState } from 'react';
import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer, Legend } from 'recharts';

const YieldDashboard = () => {
  const [data, setData] = useState([]);

  useEffect(() => {
    fetch('http://localhost:5000/api/yield')
      .then(res => res.json())
      .then(json => {
        // Transform {PASS: 450, FAIL: 50} into [{name: 'PASS', value: 450}, ...]
        const formattedData = Object.keys(json).map(key => ({
          name: key,
          value: json[key]
        }));
        setData(formattedData);
      });
  }, []);

  const COLORS = ['#FF4444', '#00C49F']; // Red for FAIL, Green for PASS

  return (
    <div style={{ width: '100%', height: 400, textAlign: 'center' }}>
      <h2>TI Manufacturing Yield Real-Time Monitor</h2>
      <ResponsiveContainer>
        <PieChart>
          <Pie
            data={data}
            innerRadius={60}
            outerRadius={100}
            paddingAngle={5}
            dataKey="value"
          >
            {data.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
            ))}
          </Pie>
          <Tooltip />
          <Legend />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
};

export default YieldDashboard;