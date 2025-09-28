// SupplyChainMap.jsx

import React, { useState, useEffect } from 'react';

const cities = [
  { id: "NYC", name: "New York", x: 184.3, y: 98.0 },
  { id: "LA", name: "Los Angeles", x: 107.4, y: 111.3 },
  { id: "London", name: "London", x: 312.8, y: 76.6 },
  { id: "Paris", name: "Paris", x: 317.1, y: 81.8 },
  { id: "Berlin", name: "Berlin", x: 336.3, y: 74.5 },
  { id: "Tokyo", name: "Tokyo", x: 556.0, y: 108.0 },
  { id: "Shanghai", name: "Shanghai", x: 524.2, y: 116.9 },
  { id: "Dubai", name: "Dubai", x: 409.2, y: 128.7 },
  { id: "Mumbai", name: "Mumbai", x: 439.7, y: 141.1 },
  { id: "Singapore", name: "Singapore", x: 493.5, y: 176.3 },
  { id: "Sydney", name: "Sydney", x: 555.9, y: 246.4 },
  { id: "Cairo", name: "Cairo", x: 367.3, y: 117.2 },
  { id: "Lagos", name: "Lagos", x: 318.9, y: 150.0 },
  { id: "SaoPaulo", name: "São Paulo", x: 246.9, y: 200.8 },
  { id: "Mexico", name: "Mexico City", x: 140.6, y: 140.4 },
  { id: "Rotterdam", name: "Rotterdam", x: 325.2, y: 72.8 },
  { id: "Hamburg", name: "Hamburg", x: 339.9, y: 70.5 },
  { id: "Antwerp", name: "Antwerp", x: 320.0, y: 75.2 },
  { id: "Frankfurt", name: "Frankfurt", x: 332.5, y: 79.2 },
  { id: "HongKong", name: "Hong Kong", x: 515.8, y: 150.2 },
  { id: "Busan", name: "Busan", x: 546.7, y: 102.5 },
  { id: "Bangkok", name: "Bangkok", x: 479.5, y: 145.3 },
  { id: "Jakarta", name: "Jakarta", x: 490.5, y: 190.2 },
  { id: "Durban", name: "Durban", x: 364.2, y: 210.0 },
  { id: "Houston", name: "Houston", x: 155.5, y: 130.5 }
];

const edges = [
  { from: "NYC", to: "London", hardship: 3 },
  { from: "NYC", to: "LA", hardship: 4 },
  { from: "NYC", to: "Mexico", hardship: 5 },
  { from: "London", to: "Paris", hardship: 2 },
  { from: "London", to: "Berlin", hardship: 3 },
  { from: "Paris", to: "Berlin", hardship: 2 },
  { from: "Berlin", to: "Dubai", hardship: 0 },
  { from: "Dubai", to: "Mumbai", hardship: 3 },
  { from: "Dubai", to: "Cairo", hardship: 2 },
  { from: "Mumbai", to: "Singapore", hardship: 4 },
  { from: "Singapore", to: "Tokyo", hardship: 4 },
  { from: "Singapore", to: "Shanghai", hardship: 2 },
  { from: "Tokyo", to: "Shanghai", hardship: 2 },
  { from: "Shanghai", to: "Tokyo", hardship: 2 },
  { from: "Sydney", to: "Singapore", hardship: 5 },
  { from: "Cairo", to: "Lagos", hardship: 4 },
  { from: "LA", to: "Mexico", hardship: 3 },
  { from: "Mexico", to: "SaoPaulo", hardship: 6 },
  { from: "London", to: "Cairo", hardship: 4 },
  { from: "Paris", to: "Cairo", hardship: 3 },
  { from: "Mumbai", to: "Dubai", hardship: 5 },
  { from: "Singapore", to: "Sydney", hardship: 5 },
  { from: "LA", to: "Tokyo", hardship: 7 },
  { from: "NYC", to: "SaoPaulo", hardship: 8 },
  { from: "Sydney", to: "SaoPaulo", hardship: 7 },
  { from: "Sydney", to: "Lagos", hardship: 6 },
  { from: "SaoPaulo", to: "Lagos", hardship: 5 },
  { from: "Rotterdam", to: "London", hardship: 2 },
  { from: "Rotterdam", to: "Antwerp", hardship: 1 },
  { from: "Rotterdam", to: "Hamburg", hardship: 2 },
  { from: "Hamburg", to: "Berlin", hardship: 2 },
  { from: "Frankfurt", to: "Berlin", hardship: 2 },
  { from: "Frankfurt", to: "Paris", hardship: 2 },
  { from: "Antwerp", to: "Paris", hardship: 2 },
  { from: "HongKong", to: "Shanghai", hardship: 2 },
  { from: "HongKong", to: "Singapore", hardship: 3 },
  { from: "HongKong", to: "Tokyo", hardship: 3 },
  { from: "Busan", to: "Tokyo", hardship: 2 },
  { from: "Busan", to: "Shanghai", hardship: 2 },
  { from: "Bangkok", to: "Singapore", hardship: 2 },
  { from: "Bangkok", to: "Jakarta", hardship: 3 },
  { from: "Jakarta", to: "Singapore", hardship: 2 },
  { from: "Durban", to: "Lagos", hardship: 5 },
  { from: "Durban", to: "Cairo", hardship: 7 },
  { from: "Houston", to: "NYC", hardship: 3 },
  { from: "Houston", to: "Mexico", hardship: 2 },
  { from: "Houston", to: "SaoPaulo", hardship: 7 }
];


const buildGraph = () => {
  const graph = {};
  cities.forEach(city => { graph[city.id] = []; });
  edges.forEach(edge => {
    graph[edge.from].push({ node: edge.to, weight: edge.hardship });
    graph[edge.to].push({ node: edge.from, weight: edge.hardship });
  });
  return graph;
};

const dijkstra = (graph, start, end) => {
  const distances = {};
  const previous = {};
  const unvisited = new Set();
  cities.forEach(city => {
    distances[city.id] = city.id === start ? 0 : Infinity;
    previous[city.id] = null;
    unvisited.add(city.id);
  });
  while (unvisited.size > 0) {
    let current = null;
    let minDistance = Infinity;
    unvisited.forEach(node => {
      if (distances[node] < minDistance) {
        minDistance = distances[node];
        current = node;
      }
    });
    if (current === null || distances[current] === Infinity) break;
    unvisited.delete(current);
    if (current === end) break;
    graph[current].forEach(neighbor => {
      if (unvisited.has(neighbor.node)) {
        const newDistance = distances[current] + neighbor.weight;
        if (newDistance < distances[neighbor.node]) {
          distances[neighbor.node] = newDistance;
          previous[neighbor.node] = current;
        }
      }
    });
  }
  const path = [];
  let curr = end;
  while (curr !== null) {
    path.unshift(curr);
    curr = previous[curr];
  }
  return distances[end] === Infinity ? { path: [], distance: 0 } : { path, distance: distances[end] };
};

// Function to find closest city based on location name
const findClosestCity = (locationName) => {
  if (!locationName) return '';
  
  const locationLower = locationName.toLowerCase();
  
  // Direct matches first
  const directMatch = cities.find(city => 
    city.name.toLowerCase().includes(locationLower) || 
    locationLower.includes(city.name.toLowerCase())
  );
  
  if (directMatch) return directMatch.id;
  
  // Common location mappings
  const locationMappings = {
    'usa': 'NYC',
    'america': 'NYC',
    'united states': 'NYC',
    'california': 'LA', 
    'china': 'Shanghai',
    'japan': 'Tokyo',
    'india': 'Mumbai',
    'uk': 'London',
    'united kingdom': 'London',
    'england': 'London',
    'france': 'Paris',
    'germany': 'Berlin',
    'uae': 'Dubai',
    'united arab emirates': 'Dubai',
    'australia': 'Sydney',
    'brazil': 'SaoPaulo',
    'egypt': 'Cairo',
    'nigeria': 'Lagos',
    'mexico': 'Mexico',
    'netherlands': 'Rotterdam',
    'south korea': 'Busan',
    'korea': 'Busan',
    'thailand': 'Bangkok',
    'indonesia': 'Jakarta',
    'south africa': 'Durban',
    'texas': 'Houston'
  };
  
  for (const [key, cityId] of Object.entries(locationMappings)) {
    if (locationLower.includes(key)) {
      return cityId;
    }
  }
  
  return '';
};

const SupplyChainMap = ({ 
  sellerLocation = '', 
  importLocation = '', 
  selectedComponent = ''
}) => {
  const [startCity, setStartCity] = useState('');
  const [endCity, setEndCity] = useState('');
  const [safestPath, setSafestPath] = useState([]);
  const [totalHardship, setTotalHardship] = useState(0);

  // Auto-populate cities based on props
  useEffect(() => {
    if (sellerLocation) {
      const matchedCity = findClosestCity(sellerLocation);
      if (matchedCity) {
        setStartCity(matchedCity);
      }
    }
  }, [sellerLocation]);

  useEffect(() => {
    if (importLocation) {
      const matchedCity = findClosestCity(importLocation);
      if (matchedCity) {
        setEndCity(matchedCity);
      }
    }
  }, [importLocation]);

  // Auto-calculate route when both cities are set
  useEffect(() => {
    if (startCity && endCity && startCity !== endCity) {
      const graph = buildGraph();
      const result = dijkstra(graph, startCity, endCity);
      setSafestPath(result.path);
      setTotalHardship(result.distance);
    }
  }, [startCity, endCity]);

  const getCityCoords = cityId => {
    const city = cities.find(c => c.id === cityId);
    return city ? { x: city.x, y: city.y } : { x: 0, y: 0 };
  };

  const isEdgeInPath = (from, to) => {
    for (let i = 0; i < safestPath.length - 1; i++) {
      if (
        (safestPath[i] === from && safestPath[i + 1] === to) ||
        (safestPath[i] === to && safestPath[i + 1] === from)
      ) return true;
    }
    return false;
  };

  return (
    <div className="w-full">
      {/* REMOVED: Current Analysis section */}
      {/* REMOVED: No Analysis Data warning section */}

      {/* Map container with image background */}
      <div
        className="relative rounded-lg overflow-hidden flex justify-center items-center bg-white border shadow-lg mb-4"
        style={{
          maxWidth: '1000px',
          aspectRatio: '2/1',
          minHeight: '400px',
          margin: '0 auto',
          background: '#EFF6FF',
          borderColor: '#dbeafe',
          boxShadow: '0 4px 24px #0002',
          position: 'relative',
        }}
      >
        {/* Background image fills container */}
        <div
          style={{
            position: 'absolute',
            inset: 0,
            width: '100%',
            height: '100%',
            backgroundImage: "url('/world.jpg')",
            backgroundSize: 'cover',
            backgroundPosition: 'center',
            pointerEvents: 'none',
            opacity: 0.28,
            zIndex: 1,
          }}
        />

        {/* SVG overlay for cities and edges */}
        <svg
          viewBox="0 0 650 258"
          style={{
            position: 'absolute',
            inset: 0,
            width: '100%',
            height: '100%',
            zIndex: 2,
          }}
        >
          {edges.map((edge, i) => {
            const from = getCityCoords(edge.from);
            const to = getCityCoords(edge.to);
            const isInPath = isEdgeInPath(edge.from, edge.to);
            return (
              <g key={i}>
                <line
                  x1={from.x}
                  y1={from.y}
                  x2={to.x}
                  y2={to.y}
                  stroke={isInPath ? "#22c55e" : "#6b7280"}
                  strokeWidth={isInPath ? 3 : 1.5}
                  opacity={isInPath ? 0.9 : 0.35}
                  strokeDasharray={isInPath ? "none" : "7,6"}
                />
                {isInPath && (
                  <text
                    x={(from.x + to.x) / 2}
                    y={(from.y + to.y) / 2 - 3}
                    fill="#059669"
                    fontWeight="600"
                    fontSize="7"
                    textAnchor="middle"
                    style={{ textShadow: '1px 1px 3px #fff6' }}
                  >
                    {edge.hardship}
                  </text>
                )}
              </g>
            );
          })}
          {cities.map(city => {
            const isSelected = city.id === startCity || city.id === endCity;
            const isInPath = safestPath.includes(city.id);
            return (
              <g key={city.id}>
                <circle
                  cx={city.x}
                  cy={city.y}
                  r={isSelected ? 5 : 3}
                  fill={isSelected ? "#3b82f6" : isInPath ? "#22c55e" : "#dc2626"}
                  stroke="#fff"
                  strokeWidth="1.5"
                  style={{ filter: "drop-shadow(0 1px 1px #0003)" }}
                />
                <rect
                  x={city.x - city.name.length * 1.5}
                  y={city.y - 14}
                  width={city.name.length * 3}
                  height={8}
                  fill="rgba(255,255,255,0.95)"
                  rx={1.5}
                  stroke="rgba(0,0,0,0.06)"
                  strokeWidth={0.2}
                />
                <text
                  x={city.x}
                  y={city.y - 7}
                  textAnchor="middle"
                  fontSize={6}
                  fill="#1f2937"
                  fontWeight={600}
                >
                  {city.name}
                </text>
              </g>
            );
          })}
        </svg>
      </div>

      {/* Results - only show when route is calculated */}
      {safestPath.length > 0 && (
        <div className="bg-white rounded-lg shadow-md p-5 w-full max-w-2xl mx-auto" style={{ textAlign: 'center' }}>
          <h3 className="text-lg font-semibold text-gray-800 mb-1">Safest Route Found</h3>
          <div className="text-gray-700">
            <p>
              <span className="font-medium">Path:</span>{' '}
              <span className="text-gray-900">
                {safestPath.map(cityId => {
                  const city = cities.find(c => c.id === cityId);
                  return city ? city.name : cityId;
                }).join(' → ')}
              </span>
            </p>
            <p className="mt-2">
              <span className="font-medium">Total Hardship Value:</span>{' '}
              <span className="text-blue-600 font-semibold">{totalHardship}</span>
            </p>
            <p className="mt-1 text-gray-500 text-xs">
              Lower hardship values indicate safer supply chain routes
            </p>
          </div>
        </div>
      )}
    </div>
  );
};

export default SupplyChainMap;
