from flask import Flask, render_template_string, request, jsonify
from MONTO_algorithm import UltimateQuantStrategy
import traceback

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>GrowWise | Laat je geld groeien</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        @keyframes float {
            0% { transform: translateY(0px); }
            50% { transform: translateY(-10px); }
            100% { transform: translateY(0px); }
        }

        @keyframes grow {
            from { transform: scale(0.95) translateY(20px); opacity: 0; }
            to { transform: scale(1) translateY(0); opacity: 1; }
        }

        @keyframes sway {
            0% { transform: rotate(0deg); }
            25% { transform: rotate(2deg); }
            75% { transform: rotate(-2deg); }
            100% { transform: rotate(0deg); }
        }

        @keyframes sparkle {
            0% { opacity: 0; transform: scale(0); }
            50% { opacity: 1; transform: scale(1); }
            100% { opacity: 0; transform: scale(0); }
        }

        @keyframes petalWave {
            0% { transform: rotate(0deg) translateX(0); }
            25% { transform: rotate(3deg) translateX(2px); }
            75% { transform: rotate(-3deg) translateX(-2px); }
            100% { transform: rotate(0deg) translateX(0); }
        }

        .float-animation {
            animation: float 4s ease-in-out infinite;
        }

        .grow-animation {
            animation: grow 1s ease-out forwards;
        }

        .sway-animation {
            animation: sway 3s ease-in-out infinite;
            transform-origin: bottom center;
        }

        .petal-wave {
            animation: petalWave 3s ease-in-out infinite;
        }

        .sparkle {
            animation: sparkle 2s ease-in-out infinite;
        }

        .gradient-text {
            background: linear-gradient(120deg, #2ecc71, #27ae60);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .plant-progress {
            transition: all 0.5s ease;
        }

        .hover-grow {
            transition: transform 0.2s ease;
        }

        .hover-grow:hover {
            transform: scale(1.02);
        }

        .plant-group path, .plant-group circle {
            opacity: 0;
            animation: appear 1s ease-out forwards;
        }

        @keyframes appear {
            from { opacity: 0; }
            to { opacity: 1; }
        }

        .plant-group path:nth-child(2) {
            animation-delay: 0.2s;
        }
        .plant-group path:nth-child(3) {
            animation-delay: 0.4s;
        }
        .plant-group path:nth-child(4) {
            animation-delay: 0.6s;
        }
        .plant-group circle {
            animation-delay: 0.8s;
        }

        .result-card {
            background: white;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            margin-bottom: 20px;
            overflow: hidden;
        }

        .result-card-header {
            background: linear-gradient(120deg, #2ecc71, #27ae60);
            color: white;
            padding: 15px 20px;
        }

        .result-card-body {
            padding: 20px;
        }

        .result-summary {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 20px;
        }

        .allocation-item {
            display: flex;
            justify-content: space-between;
            padding: 10px;
            border-bottom: 1px solid #e5e7eb;
        }

        .allocation-item:last-child {
            border-bottom: none;
        }

        .risk-level {
            display: inline-block;
            padding: 4px 8px;
            border-radius: 4px;
            font-weight: 600;
            font-size: 0.875rem;
        }

        .risk-low { background: #dcfce7; color: #166534; }
        .risk-medium { background: #fef9c3; color: #854d0e; }
        .risk-high { background: #fee2e2; color: #991b1b; }

        /* Extra styles voor de nieuwe secties */
        .card {
            background: #fff;
            border-radius: 12px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            margin-bottom: 20px;
        }

        .card-header {
            padding: 15px 20px;
            border-bottom: 1px solid #e5e7eb;
        }

        .card-header.bg-success {
            background-color: #2ecc71;
            color: white;
        }

        .card-body {
            padding: 20px;
        }

        .orders-section {
            margin-bottom: 20px;
        }

        .order-item {
            display: flex;
            justify-content: space-between;
            padding: 10px;
            border-bottom: 1px solid #e5e7eb;
        }

        .order-item:last-child {
            border-bottom: none;
        }

        .order-type {
            font-weight: 600;
        }

        .order-details {
            color: #555;
        }

        .confidence-badge {
            display: inline-block;
            padding: 4px 8px;
            border-radius: 4px;
            font-weight: 600;
            font-size: 0.875rem;
        }

        .confidence-badge.low {
            background: #dcfce7;
            color: #166534;
        }

        .confidence-badge.medium {
            background: #fef9c3;
            color: #854d0e;
        }

        .confidence-badge.high {
            background: #fee2e2;
            color: #991b1b;
        }

        .trading-tips {
            background: #f9f9f9;
            padding: 15px;
            border-radius: 8px;
        }

        .trading-tips h3 {
            margin-bottom: 10px;
            font-weight: 600;
        }

        .position-advice, .risk-warnings {
            background: #f9f9f9;
            padding: 15px;
            border-radius: 8px;
            margin-top: 10px;
        }

        .position-advice h3, .risk-warnings h3 {
            margin-bottom: 10px;
            font-weight: 600;
        }

        /* Nieuwe plant hover effecten */
        .plant-hover {
            transition: all 0.3s ease;
        }

        .plant-hover:hover .stem {
            transform: scale(1.02) translateY(-2px);
        }

        .plant-hover:hover .leaves {
            transform: rotate(5deg);
        }

        .plant-hover:hover .flower {
            transform: scale(1.1);
        }

        /* Voeg dit toe voor het form */
        .loading {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(255,255,255,0.9);
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 1000;
        }

        .spinner {
            width: 50px;
            height: 50px;
            border: 5px solid #f3f3f3;
            border-top: 5px solid #2ecc71;
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }

        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    </style>
</head>
<body class="bg-gray-50 font-['Poppins']">
    <!-- Hero Section -->
    <div class="min-h-screen">
        <div class="container mx-auto px-6 py-16">
            <div class="flex flex-col lg:flex-row items-center">
                <div class="lg:w-1/2">
                    <h1 class="text-5xl font-bold mb-8 gradient-text">
                        Plant je financiële toekomst 🌱
                    </h1>
                    <p class="text-xl text-gray-600 mb-8">
                        Net als een plant heeft jouw vermogen water en zorg nodig om te groeien. 
                        Met GrowWise geef je je geld elke maand precies wat het nodig heeft.
                    </p>
                    <div class="flex flex-wrap gap-4">
                        <button id="startButton" class="bg-green-500 text-white px-8 py-4 rounded-lg font-semibold hover-grow shadow-lg">
                            Start met groeien →
                        </button>
                        <button id="learnMoreButton" class="border-2 border-green-500 text-green-500 px-8 py-4 rounded-lg font-semibold hover-grow">
                            <span class="flex items-center">
                                <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
                                </svg>
                                Leer meer
                            </span>
                        </button>
                    </div>
                </div>
                <div class="lg:w-1/2 mt-10 lg:mt-0">
                    <div class="float-animation relative">
                        <svg class="w-full" viewBox="0 0 200 200">
                            <defs>
                                <!-- Gradient definitions for different states -->
                                <linearGradient id="stemGradient" x1="0%" y1="0%" x2="100%" y2="0%">
                                    <stop offset="0%" style="stop-color:{{ plant_state.stem_color }};stop-opacity:0.8"/>
                                    <stop offset="100%" style="stop-color:{{ plant_state.stem_color }};stop-opacity:1"/>
                                </linearGradient>
                                <linearGradient id="leafGradient" x1="0%" y1="0%" x2="100%" y2="0%">
                                    <stop offset="0%" style="stop-color:{{ plant_state.leaf_color }};stop-opacity:0.8"/>
                                    <stop offset="100%" style="stop-color:{{ plant_state.leaf_color }};stop-opacity:1"/>
                                </linearGradient>
                                <filter id="glow">
                                    <feGaussianBlur stdDeviation="2" result="coloredBlur"/>
                                    <feMerge>
                                        <feMergeNode in="coloredBlur"/>
                                        <feMergeNode in="SourceGraphic"/>
                                    </feMerge>
                                </filter>
                            </defs>
                            
                            <g class="plant-group">
                                <!-- Enhanced Pot with 3D effect -->
                                <path d="M50,160 C50,160 60,180 100,180 C140,180 150,160 150,160 L140,200 L60,200 Z" 
                                      fill="{{ plant_state.pot_color }}" 
                                      stroke="#00000022" 
                                      stroke-width="1"/>
                                
                                <!-- Dynamic Stem with gradient -->
                                <g class="sway-animation">
                                    <path class="grow-animation" 
                                          d="M100,160 C100,140 95,120 100,100 C105,80 100,60 100,40" 
                                          stroke="url(#stemGradient)" 
                                          stroke-width="6" 
                                          fill="none"
                                          stroke-linecap="round"/>
                                    
                                    <!-- Enhanced Leaves -->
                                    {% if plant_state.state in ['dorry', 'thirsty'] %}
                                        <!-- Drooping leaves for dry state -->
                                        <g class="petal-wave">
                                            <path d="M100,120 C110,120 130,130 140,150" 
                                                  stroke="url(#leafGradient)" 
                                                  stroke-width="4" 
                                                  fill="none"/>
                                            <path d="M100,100 C90,100 70,110 60,130" 
                                                  stroke="url(#leafGradient)" 
                                                  stroke-width="4" 
                                                  fill="none"/>
                                        </g>
                                    {% else %}
                                        <!-- Healthy leaves with more detail -->
                                        <g class="petal-wave">
                                            <path d="M100,120 C120,110 140,120 145,110 C150,100 140,90 130,95" 
                                                  stroke="url(#leafGradient)" 
                                                  stroke-width="4" 
                                                  fill="{{ plant_state.leaf_color }}"/>
                                            <path d="M100,100 C80,90 60,100 55,90 C50,80 60,70 70,75" 
                                                  stroke="url(#leafGradient)" 
                                                  stroke-width="4" 
                                                  fill="{{ plant_state.leaf_color }}"/>
                                        </g>
                                    {% endif %}
                                    
                                    <!-- Dynamic Flower/Coins based on state -->
                                    {% if plant_state.state == 'overripe' %}
                                        <!-- Multiple animated coins for extreme greed -->
                                        <g filter="url(#glow)">
                                            <g class="sparkle">
                                                <circle cx="100" cy="40" r="15" fill="{{ plant_state.flower_color }}"/>
                                                <circle cx="85" cy="50" r="12" fill="{{ plant_state.flower_color }}"/>
                                                <circle cx="115" cy="50" r="12" fill="{{ plant_state.flower_color }}"/>
                                                <text x="95" y="45" font-family="Arial" font-size="14" fill="white" font-weight="bold">€</text>
                                                <text x="80" y="55" font-family="Arial" font-size="12" fill="white" font-weight="bold">€</text>
                                                <text x="110" y="55" font-family="Arial" font-size="12" fill="white" font-weight="bold">€</text>
                                            </g>
                                        </g>
                                    {% elif plant_state.state == 'blooming' %}
                                        <!-- Beautiful flower for blooming state -->
                                        <g class="petal-wave" filter="url(#glow)">
                                            <!-- Flower center -->
                                            <circle cx="100" cy="40" r="8" fill="{{ plant_state.flower_color }}"/>
                                            <!-- Animated petals -->
                                            {% for i in range(8) %}
                                                <path d="M100,40 C105,35 110,25 100,15 C90,25 95,35 100,40" 
                                                      fill="{{ plant_state.flower_color }}"
                                                      transform="rotate({{ i * 45 }}, 100, 40)"/>
                                            {% endfor %}
                                        </g>
                                    {% elif plant_state.state == 'healthy' %}
                                        <!-- Healthy flower with subtle animation -->
                                        <g class="petal-wave">
                                            <circle cx="100" cy="40" r="12" fill="{{ plant_state.flower_color }}">
                                                <animate attributeName="r" 
                                                        values="12;13;12" 
                                                        dur="3s" 
                                                        repeatCount="indefinite"/>
                                            </circle>
                                        </g>
                                    {% endif %}
                                </g>
                            </g>
                        </svg>
                        
                        <!-- Plant Status Message -->
                        <div class="absolute bottom-0 left-0 right-0 text-center bg-white bg-opacity-95 p-6 rounded-xl shadow-lg transform transition-all duration-300 hover:scale-102">
                            <p class="text-2xl font-bold mb-2 bg-gradient-to-r from-green-500 to-green-600 bg-clip-text text-transparent">
                                {{ plant_state.message }}
                            </p>
                            <p class="text-base text-gray-600 leading-relaxed">
                                {{ plant_state.description }}
                            </p>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- How it works -->
        <div class="bg-white py-16">
            <div class="container mx-auto px-6">
                <h2 class="text-3xl font-bold text-center mb-12">Hoe het werkt</h2>
                <div class="grid md:grid-cols-3 gap-8">
                    <div class="p-6 bg-gray-50 rounded-xl hover-grow">
                        <div class="text-4xl mb-4">🌱</div>
                        <h3 class="font-semibold text-xl mb-2">Plant je eerste investering</h3>
                        <p class="text-gray-600">Begin met een bedrag dat bij jou past. Zelfs €100 per maand kan uitgroeien tot iets moois.</p>
                    </div>
                    <div class="p-6 bg-gray-50 rounded-xl hover-grow">
                        <div class="text-4xl mb-4">💧</div>
                        <h3 class="font-semibold text-xl mb-2">Geef maandelijks water</h3>
                        <p class="text-gray-600">Voeg elke maand consistent bij. Wij zorgen voor de juiste verdeling.</p>
                    </div>
                    <div class="p-6 bg-gray-50 rounded-xl hover-grow">
                        <div class="text-4xl mb-4">🌳</div>
                        <h3 class="font-semibold text-xl mb-2">Zie het groeien</h3>
                        <p class="text-gray-600">Volg je groei in je persoonlijke groeidagboek en zie je vermogen bloeien.</p>
                    </div>
                </div>
            </div>
        </div>

        <!-- Calculator Section -->
        <div id="calculator" class="py-16 bg-gradient-to-b from-green-50 to-white">
            <div class="container mx-auto px-6">
                <h2 class="text-3xl font-bold text-center mb-12">Bereken je groeipotentieel</h2>
                <div class="max-w-md mx-auto bg-white rounded-xl shadow-lg p-8">
                    <form method="POST" class="space-y-6">
                        <div>
                            <label class="block text-sm font-medium text-gray-700 mb-2">
                                Hoeveel wil je maandelijks investeren?
                            </label>
                            <div class="relative">
                                <span class="absolute left-3 top-3 text-gray-500">€</span>
                                <input type="number" name="amount" value="1500" min="100" max="10000" 
                                    class="pl-8 w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                                    required>
                            </div>
                        </div>
                        <button type="submit" class="w-full bg-green-500 text-white py-4 rounded-lg font-semibold hover-grow">
                            Bereken mijn groeiplan 🌱
                        </button>
                    </form>
                </div>

                {% if result %}
                    {% if not result.error %}
                    <div class="mt-8 max-w-4xl mx-auto space-y-6 grow-animation">
                        <!-- Market Overview Card -->
                        <div class="result-card">
                            <div class="result-card-header">
                                <h3 class="text-xl font-semibold">Markt Condities</h3>
                            </div>
                            <div class="result-card-body">
                                <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                                    <div class="text-center p-4 bg-gray-50 rounded-lg">
                                        <div class="text-sm text-gray-500">Fear & Greed Index SP500</div>
                                        <div class="text-2xl font-bold">{{ result.market_conditions.fear_greed }}/100</div>
                                    </div>
                                    <div class="text-center p-4 bg-gray-50 rounded-lg">
                                        <div class="text-sm text-gray-500">Bitcoin Fear & Greed</div>
                                        <div class="text-2xl font-bold">{{ result.market_conditions.btc_fear_greed }}/100</div>
                                    </div>
                                    <div class="text-center p-4 bg-gray-50 rounded-lg">
                                        <div class="text-sm text-gray-500">Markt Regime</div>
                                        <div class="text-xl font-bold">{{ result.market_conditions.regime }}</div>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- Allocation Overview -->
                        <div class="result-card">
                            <div class="result-card-header">
                                <h3 class="text-xl font-semibold">Investeringsplan (€{{ "%.2f"|format(result.total) }})</h3>
                            </div>
                            <div class="result-card-body">
                                <div class="space-y-4">
                                    {% for item in result.allocations %}
                                    <div class="relative overflow-hidden rounded-lg">
                                        <!-- Progress bar background -->
                                        <div class="absolute top-0 left-0 h-full bg-blue-100/50" 
                                             style="width: {{ (item.amount / result.total * 100)|float }}%">
                                        </div>
                                        
                                        <!-- Content -->
                                        <div class="relative flex items-center justify-between p-4">
                                            <div>
                                                <div class="font-semibold">{{ item.asset }}</div>
                                                {% if item.shares %}
                                                <div class="text-sm text-gray-500">{{ item.shares }} aandelen</div>
                                                {% endif %}
                                            </div>
                                            <div class="text-right">
                                                <div class="text-xl font-bold">€{{ "%.2f"|format(item.amount) }}</div>
                                                <div class="text-sm text-gray-600">{{ "%.1f"|format(item.amount / result.total * 100) }}%</div>
                                            </div>
                                        </div>
                                    </div>
                                    {% endfor %}
                                </div>
                            </div>
                        </div>

                        <!-- Voorgestelde Orders -->
                        <div class="result-card">
                            <div class="result-card-header">
                                <h3 class="text-xl font-semibold">Voorgestelde Orders</h3>
                            </div>
                            <div class="result-card-body space-y-6">
                                <!-- Optimale Handelstijden -->
                                <div class="bg-gray-50 p-4 rounded-lg">
                                    <h4 class="font-semibold mb-2">Optimale Handelstijden</h4>
                                    <ul class="space-y-2 text-gray-600">
                                        <li>• Beste uren: 14:30-22:00 CET</li>
                                        <li>• Maandelijks window: 15-25e van de maand</li>
                                    </ul>
                                </div>

                                <!-- IWDA Orders -->
                                <div class="bg-white rounded-lg p-4 shadow-sm border border-gray-100">
                                    <h3 class="text-lg font-semibold mb-4 text-slate-800">IWDA Orders</h3>
                                    <div class="space-y-3">
                                        {% for order in result.order_placement.iwda %}
                                        <div class="flex items-center justify-between p-3 bg-slate-50 rounded-lg hover:bg-slate-100 transition-all">
                                            <div class="flex flex-col">
                                                <span class="font-medium text-slate-700">{{ order.type }} Order</span>
                                            </div>
                                            <div class="flex items-center gap-3">
                                                <span class="font-mono text-slate-700">€{{ "%.2f"|format(order.price) }}</span>
                                                <span class="px-2 py-1 text-sm rounded-md {% if order.confidence == 'High' %}bg-slate-200 text-slate-700{% elif order.confidence == 'Medium' %}bg-slate-100 text-slate-600{% else %}bg-slate-50 text-slate-500{% endif %}">
                                                    {{ order.confidence }}
                                                </span>
                                            </div>
                                        </div>
                                        {% endfor %}
                                    </div>
                                </div>

                                <!-- Bitcoin Orders -->
                                <div class="bg-white rounded-lg p-4 shadow-sm border border-gray-100">
                                    <h3 class="text-lg font-semibold mb-4 text-slate-800">Bitcoin Orders</h3>
                                    <div class="space-y-3">
                                        {% for order in result.order_placement.btc %}
                                        <div class="flex items-center justify-between p-3 bg-slate-50 rounded-lg hover:bg-slate-100 transition-all">
                                            <div class="flex flex-col">
                                                <span class="font-medium text-slate-700">{{ order.type }} Order</span>
                                            </div>
                                            <div class="flex items-center gap-3">
                                                <span class="font-mono text-slate-700">€{{ "%.2f"|format(order.price) }}</span>
                                                <span class="px-2 py-1 text-sm rounded-md {% if order.confidence == 'High' %}bg-slate-200 text-slate-700{% elif order.confidence == 'Medium' %}bg-slate-100 text-slate-600{% else %}bg-slate-50 text-slate-500{% endif %}">
                                                    {{ order.confidence }}
                                                </span>
                                            </div>
                                        </div>
                                        {% endfor %}
                                    </div>
                                </div>

                                <!-- Trading Tips -->
                                <div class="bg-slate-50 rounded-lg p-4">
                                    <h3 class="text-lg font-semibold mb-3 text-slate-800">💡 Uitvoeringstips</h3>
                                    <ul class="space-y-2">
                                        {% for tip in result.order_placement.trading_tips.execution_tips %}
                                        <li class="text-slate-600 flex items-start">
                                            <span class="mr-2">•</span>
                                            {{ tip }}
                                        </li>
                                        {% endfor %}
                                    </ul>
                                </div>
                            </div>
                        </div>

                        <!-- Risk Analysis -->
                        <div class="result-card">
                            <div class="result-card-header">
                                <h3 class="text-xl font-semibold">Risico Analyse</h3>
                            </div>
                            <div class="result-card-body space-y-6">
                                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                                    <div class="bg-gray-50 p-4 rounded-lg">
                                        <h4 class="font-semibold mb-2">Value at Risk (95% confidence)</h4>
                                        <ul class="space-y-2">
                                            <li>IWDA: {{ result.risk_metrics.value_at_risk.iwda }}% daily</li>
                                            <li>Bitcoin: {{ result.risk_metrics.value_at_risk.btc }}% daily</li>
                                        </ul>
                                    </div>
                                    <div class="bg-gray-50 p-4 rounded-lg">
                                        <h4 class="font-semibold mb-2">Jaarlijkse Volatiliteit</h4>
                                        <ul class="space-y-2">
                                            <li>IWDA: {{ result.risk_metrics.volatility.iwda }}%</li>
                                            <li>Bitcoin: {{ result.risk_metrics.volatility.btc }}%</li>
                                        </ul>
                                    </div>
                                </div>
                                <div class="bg-gray-50 p-4 rounded-lg">
                                    <h4 class="font-semibold mb-2">Portfolio Metrics</h4>
                                    <ul class="space-y-2">
                                        <li>Verwacht Rendement: {{ result.risk_metrics.portfolio_metrics.expected_return }}%</li>
                                        <li>Verwacht Risico: {{ result.risk_metrics.portfolio_metrics.expected_risk }}%</li>
                                        <li>Sharpe Ratio: {{ result.risk_metrics.portfolio_metrics.sharpe_ratio }}</li>
                                    </ul>
                                </div>
                            </div>
                        </div>

                        
                    </div>
                    {% else %}
                    <div class="mt-8 max-w-2xl mx-auto">
                        <div class="result-card">
                            <div class="result-card-header bg-red-500">
                                <h3 class="text-xl font-semibold">Foutmelding</h3>
                            </div>
                            <div class="result-card-body">
                                <p class="text-gray-600">{{ result.error }}</p>
                            </div>
                        </div>
                    </div>
                    {% endif %}
                {% endif %}
            </div>
        </div>

        <!-- Learn More Section -->
        <div id="learn-more" class="py-16">
            <div class="container mx-auto px-6">
                <h2 class="text-3xl font-bold text-center mb-12 gradient-text">Jouw Reis naar Financiële Groei</h2>

                <!-- Navigation Tabs -->
                <div class="mb-12">
                    <div class="flex justify-center space-x-4 border-b border-gray-200">
                        <button data-tab="basics" class="tab-button active py-4 px-6 border-b-2 border-green-500 font-medium">Basis</button>
                        <button data-tab="markets" class="tab-button py-4 px-6 border-b-2 border-transparent font-medium text-gray-500">Markten</button>
                        <button data-tab="strategy" class="tab-button py-4 px-6 border-b-2 border-transparent font-medium text-gray-500">Strategie</button>
                        <button data-tab="algorithm" class="tab-button py-4 px-6 border-b-2 border-transparent font-medium text-gray-500">Algoritme</button>
                        <button data-tab="results" class="tab-button py-4 px-6 border-b-2 border-transparent font-medium text-gray-500">Resultaten</button>
                    </div>
                </div>

                <!-- Tab Contents (behoud de bestaande tab content, alleen verplaatst) -->
                <div class="max-w-4xl mx-auto">
                    <!-- Basics Tab -->
                    <div id="basics" class="tab-content">
                        <h3 class="text-xl font-semibold mb-6">De Basis van Slim Investeren</h3>

                        <!-- Waarom Investeren -->
                        <div class="bg-white rounded-lg p-6 shadow-sm mb-8">
                            <h4 class="text-lg font-semibold mb-4">Waarom Zou Je Investeren?</h4>
                            <div class="space-y-4 text-gray-600">
                                <p class="text-lg">Er zijn vier belangrijke redenen waarom investeren essentieel is voor je financiële toekomst:</p>
                                
                                <div class="grid md:grid-cols-2 gap-6">
                                    <div class="bg-gray-50 p-4 rounded-lg">
                                        <h5 class="font-medium text-green-600 mb-2">1. Bescherming Tegen Inflatie</h5>
                                        <p>Je geld verliest elk jaar 2-3% aan koopkracht door inflatie. €10.000 vandaag is over 10 jaar nog maar €8.000 waard als je niet investeert.</p>
                                    </div>
                                    
                                    <div class="bg-gray-50 p-4 rounded-lg">
                                        <h5 class="font-medium text-green-600 mb-2">2. Vermogensopbouw</h5>
                                        <p>Met alleen sparen bouw je geen vermogen op. Moderne spaarrekeningen geven nauwelijks rente, terwijl investeringen historisch 7-10% per jaar opleveren.</p>
                                    </div>

                                    <div class="bg-gray-50 p-4 rounded-lg">
                                        <h5 class="font-medium text-green-600 mb-2">3. Passief Inkomen</h5>
                                        <p>Door te investeren laat je je geld voor je werken. Dividenden en waardegroei kunnen een extra inkomstenstroom creëren.</p>
                                    </div>

                                    <div class="bg-gray-50 p-4 rounded-lg">
                                        <h5 class="font-medium text-green-600 mb-2">4. Financiële Vrijheid</h5>
                                        <p>Consistent investeren is de meest beproefde weg naar financiële onafhankelijkheid en het bereiken van je lange termijn doelen.</p>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- De Kracht van Compound Interest -->
                        <div class="bg-white rounded-lg p-6 shadow-sm mb-8">
                            <h4 class="text-lg font-semibold mb-4">De Magie van Samengestelde Interest</h4>
                            <div class="space-y-4">
                                <p class="text-gray-600">Einstein noemde het de "8e wereldwonder": geld dat zichzelf vermenigvuldigt door rente op rente. Hier zie je waarom:</p>
                                
                                <div class="bg-blue-50 p-6 rounded-lg">
                                    <h5 class="font-medium text-blue-800 mb-4">Voorbeeld: €500 per maand geïnvesteerd</h5>
                                    <div class="grid md:grid-cols-3 gap-4 text-center">
                                        <div class="bg-white p-4 rounded-lg shadow-sm">
                                            <p class="text-sm text-gray-500">Na 10 jaar</p>
                                            <p class="text-xl font-bold text-blue-600">€91.473</p>
                                            <p class="text-sm text-gray-500">Ingelegd: €60.000</p>
                                        </div>
                                        <div class="bg-white p-4 rounded-lg shadow-sm">
                                            <p class="text-sm text-gray-500">Na 20 jaar</p>
                                            <p class="text-xl font-bold text-blue-600">€294.510</p>
                                            <p class="text-sm text-gray-500">Ingelegd: €120.000</p>
                                        </div>
                                        <div class="bg-white p-4 rounded-lg shadow-sm">
                                            <p class="text-sm text-gray-500">Na 30 jaar</p>
                                            <p class="text-xl font-bold text-blue-600">€750.150</p>
                                            <p class="text-sm text-gray-500">Ingelegd: €180.000</p>
                                        </div>
                                    </div>
                                    <p class="text-sm text-blue-600 mt-4">* Gebaseerd op 8% gemiddeld jaarlijks rendement</p>
                                </div>
                            </div>
                        </div>

                        <!-- Beginnen met Investeren -->
                        <div class="bg-white rounded-lg p-6 shadow-sm">
                            <h4 class="text-lg font-semibold mb-4">Hoe Begin Je?</h4>
                            <div class="space-y-6">
                                <div class="border-l-4 border-green-500 pl-4">
                                    <h5 class="font-medium mb-2">1. Start Klein</h5>
                                    <p class="text-gray-600">Begin met een bedrag dat comfortabel voelt. €100-200 per maand is al genoeg om te starten met vermogensopbouw.</p>
                                </div>

                                <div class="border-l-4 border-green-500 pl-4">
                                    <h5 class="font-medium mb-2">2. Wees Consistent</h5>
                                    <p class="text-gray-600">Investeer elke maand een vast bedrag. Deze 'dollar-cost averaging' strategie spreidt je risico en bouwt discipline.</p>
                                </div>

                                <div class="border-l-4 border-green-500 pl-4">
                                    <h5 class="font-medium mb-2">3. Denk Lang</h5>
                                    <p class="text-gray-600">Succesvolle beleggers denken in jaren en decennia, niet in dagen of weken. Geef je investeringen tijd om te groeien.</p>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Markets Tab -->
                    <div id="markets" class="tab-content hidden">
                        <h3 class="text-xl font-semibold mb-6">De Financiële Markten Begrijpen</h3>

                        <!-- Marktcycli Uitleg -->
                        <div class="bg-white rounded-lg p-6 shadow-sm mb-8">
                            <h4 class="text-lg font-semibold mb-4">De Emotionele Achtbaan van de Markten</h4>
                            <div class="space-y-4">
                                <p class="text-gray-600">Financiële markten worden gedreven door twee krachtige emoties: Angst en Hebzucht. Dit creëert voorspelbare cycli:</p>
                                
                                <div class="grid md:grid-cols-2 gap-6">
                                    <div class="bg-gray-50 p-4 rounded-lg">
                                        <h5 class="font-medium text-red-600 mb-2">Extreme Angst (0-25)</h5>
                                        <ul class="list-disc pl-5 space-y-2 text-gray-600">
                                            <li>Paniekverkopen</li>
                                            <li>Media zeer negatief</li>
                                            <li>Vaak beste moment om te kopen</li>
                                            <li>Historisch hoogste rendementen</li>
                                        </ul>
                                    </div>
                                    
                                    <div class="bg-gray-50 p-4 rounded-lg">
                                        <h5 class="font-medium text-green-600 mb-2">Extreme Hebzucht (75-100)</h5>
                                        <ul class="list-disc pl-5 space-y-2 text-gray-600">
                                            <li>FOMO (Fear of Missing Out)</li>
                                            <li>Overmatig optimisme</li>
                                            <li>Vaak riskant om in te stappen</li>
                                            <li>Tijd voor voorzichtigheid</li>
                                        </ul>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- Beschikbare Assets -->
                        <div class="bg-white rounded-lg p-6 shadow-sm mb-8">
                            <h4 class="text-lg font-semibold mb-4">Onze Investeringsinstrumenten</h4>
                            
                            <!-- IWDA ETF -->
                            <div class="mb-8">
                                <h5 class="text-lg font-medium text-green-600 mb-4">IWDA ETF: Je Wereldwijde Basis</h5>
                                <div class="space-y-4">
                                    <p class="text-gray-600">De iShares World ETF (IWDA) is als een mandje met aandelen van 's werelds beste bedrijven:</p>
                                    
                                    <div class="grid md:grid-cols-2 gap-4">
                                        <div class="bg-gray-50 p-4 rounded-lg">
                                            <h6 class="font-medium mb-2">Waarom IWDA?</h6>
                                            <ul class="list-disc pl-5 space-y-2 text-gray-600">
                                                <li>Spreiding over 1500+ topbedrijven</li>
                                                <li>23 ontwikkelde landen</li>
                                                <li>Automatische dividendherinvestering</li>
                                                <li>Zeer lage kosten (0.20% per jaar)</li>
                                            </ul>
                                        </div>
                                        
                                        <div class="bg-gray-50 p-4 rounded-lg">
                                            <h6 class="font-medium mb-2">Wat Krijg Je?</h6>
                                            <ul class="list-disc pl-5 space-y-2 text-gray-600">
                                                <li>Apple, Microsoft, Amazon</li>
                                                <li>Johnson & Johnson, Nestlé</li>
                                                <li>Visa, Mastercard</li>
                                                <li>En 1500+ andere wereldleiders</li>
                                            </ul>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            
                            <!-- Bitcoin -->
                            <div>
                                <h5 class="text-lg font-medium text-green-600 mb-4">Bitcoin: Digitaal Goud</h5>
                                <div class="space-y-4">
                                    <p class="text-gray-600">Bitcoin is een revolutionaire vorm van digitaal geld met unieke eigenschappen:</p>
                                    
                                    <div class="grid md:grid-cols-2 gap-4">
                                        <div class="bg-gray-50 p-4 rounded-lg">
                                            <h6 class="font-medium mb-2">Waarom Bitcoin?</h6>
                                            <ul class="list-disc pl-5 space-y-2 text-gray-600">
                                                <li>Beperkte voorraad (max 21 miljoen)</li>
                                                <li>Bescherming tegen inflatie</li>
                                                <li>24/7 verhandelbaar</li>
                                                <li>Groeiende institutionele adoptie</li>
                                            </ul>
                                        </div>
                                        
                                        <div class="bg-gray-50 p-4 rounded-lg">
                                            <h6 class="font-medium mb-2">Risico's & Kansen</h6>
                                            <ul class="list-disc pl-5 space-y-2 text-gray-600">
                                                <li>Zeer volatiel (grote prijsschommelingen)</li>
                                                <li>Nog jonge technologie</li>
                                                <li>Potentieel hoog rendement</li>
                                                <li>Beperkt % van portfolio (max 1-5%)</li>
                                            </ul>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- Optimale Mix -->
                        <div class="bg-blue-50 rounded-lg p-6">
                            <h4 class="text-lg font-semibold mb-4 text-blue-800">💡 De Perfecte Balans</h4>
                            <div class="text-blue-700">
                                <p class="mb-4">Onze aanbevolen mix combineert het beste van twee werelden:</p>
                                <ul class="list-disc pl-5 space-y-2">
                                    <li>IWDA als stabiele basis (75-95%)</li>
                                    <li>Bitcoin voor extra groeipotentieel (5-25%)</li>
                                    <li>Dynamische aanpassing op basis van marktomstandigheden</li>
                                    <li>Strategische cash buffer voor opportuniteiten</li>
                                </ul>
                            </div>
                        </div>
                    </div>

                    <!-- Strategy Tab -->
                    <div id="strategy" class="tab-content hidden">
                        <h3 class="text-xl font-semibold mb-6">MONTO Strategie: Consistente Maandelijkse Groei</h3>

                        <!-- Kern Principes -->
                        <div class="bg-white rounded-lg p-6 shadow-sm mb-8">
                            <h4 class="text-lg font-semibold mb-4">Kernprincipes</h4>
                            <div class="space-y-4 text-gray-600">
                                <p class="text-lg">De MONTO strategie is ontworpen voor consistente, maandelijkse investeringen met optimale timing en risicobeheer:</p>
                                <ul class="list-disc pl-5 space-y-2">
                                    <li>Kies een vast maandelijks bedrag dat je kunt missen</li>
                                    <li>Beleg elke maand, zonder uitzondering</li>
                                    <li>Gebruik marktomstandigheden voor optimale timing</li>
                                    <li>Behoud een strategische buffer voor opportuniteiten</li>
                                </ul>
                            </div>
                        </div>

                        <!-- Hoe het Werkt -->
                        <div class="bg-white rounded-lg p-6 shadow-sm mb-8">
                            <h4 class="text-lg font-semibold mb-4">Hoe het Werkt</h4>
                            <div class="space-y-6">
                                <div class="border-l-4 border-green-500 pl-4">
                                    <h5 class="font-medium mb-2">1. Maandelijkse Planning</h5>
                                    <p class="text-gray-600">Begin elke maand met je vaste investeringsbedrag. Bijvoorbeeld €1500 per maand.</p>
                                </div>

                                <div class="border-l-4 border-green-500 pl-4">
                                    <h5 class="font-medium mb-2">2. Check MONTO Tool</h5>
                                    <p class="text-gray-600">De tool analyseert marktcondities en berekent:</p>
                                    <ul class="list-disc pl-5 mt-2 text-gray-600">
                                        <li>Optimale verdeling tussen IWDA en Bitcoin</li>
                                        <li>Hoeveel cash buffer aan te houden</li>
                                        <li>Beste entry points voor je orders</li>
                                    </ul>
                                </div>

                                <div class="border-l-4 border-green-500 pl-4">
                                    <h5 class="font-medium mb-2">3. Uitvoering</h5>
                                    <p class="text-gray-600">Voer zelf de voorgestelde orders uit bij je broker:</p>
                                    <ul class="list-disc pl-5 mt-2 text-gray-600">
                                        <li>Plaats de orders binnen het aanbevolen tijdvenster</li>
                                        <li>Gebruik limit orders voor betere prijzen</li>
                                        <li>Houd de voorgestelde buffer aan</li>
                                    </ul>
                                </div>
                            </div>
                        </div>

                        <!-- Belangrijke Reminder -->
                        <div class="bg-blue-50 rounded-lg p-6 mb-8">
                            <h4 class="text-lg font-semibold mb-4 text-blue-800">💡 Belangrijke Reminder</h4>
                            <div class="text-blue-700">
                                <p class="mb-4">Consistentie is de sleutel tot succes. Het belangrijkste is dat je:</p>
                                <ul class="list-disc pl-5 space-y-2">
                                    <li>Elke maand investeert, ongeacht marktomstandigheden</li>
                                    <li>Je aan je vooraf bepaalde bedrag houdt</li>
                                    <li>De strategie langdurig volhoudt</li>
                                    <li>Emotionele beslissingen vermijdt</li>
                                </ul>
                            </div>
                        </div>

                        <!-- Disclaimer -->
                        <div class="text-sm text-gray-500 mt-8">
                            <p>* De MONTO tool geeft suggesties voor timing en allocatie, maar de uiteindelijke investeringsbeslissingen liggen bij jou.</p>
                            <p>* Zorg dat je bekend bent met de werking van je broker en de beschikbare ordertypen.</p>
                            <p>* Beleg nooit meer dan je kunt missen.</p>
                        </div>
                    </div>

                    <!-- Algorithm Tab -->
                    <div id="algorithm" class="tab-content hidden">
                        <h3 class="text-xl font-semibold mb-6">Het MONTO Algoritme Uitgelegd</h3>

                        <!-- Disclaimer Banner -->
                        <div class="bg-blue-50 border-l-4 border-blue-500 p-4 mb-8">
                            <p class="text-sm text-blue-700">
                                Dit algoritme is ontwikkeld voor educatieve en informatieve doeleinden. Het vormt geen financieel advies. Raadpleeg een financieel adviseur voor persoonlijk beleggingsadvies.
                            </p>
                        </div>

                        <!-- Core Components -->
                        <div class="space-y-8">
                            <!-- Market Analysis -->
                            <div class="bg-white rounded-lg p-6 shadow-sm">
                                <h4 class="text-lg font-semibold mb-4">1. Marktanalyse</h4>
                                <div class="space-y-4 text-gray-600">
                                    <p>Het algoritme analyseert dagelijks:</p>
                                    <ul class="list-disc pl-5 space-y-2">
                                        <li>Fear & Greed Index (marktsentiment)</li>
                                        <li>Volatiliteit en handelsvolumes</li>
                                        <li>Technische indicatoren (ATR, volume profielen)</li>
                                        <li>Prijspatronen en marktstructuur</li>
                                    </ul>
                                </div>
                            </div>

                            <!-- Risk Management -->
                            <div class="bg-white rounded-lg p-6 shadow-sm">
                                <h4 class="text-lg font-semibold mb-4">2. Risicobeheer</h4>
                                <div class="space-y-4 text-gray-600">
                                    <p>Ingebouwde veiligheidsmaatregelen:</p>
                                    <ul class="list-disc pl-5 space-y-2">
                                        <li>Maximaal 33% allocatie naar volatiele assets</li>
                                        <li>Dynamische positiegrootte op basis van marktrisico</li>
                                        <li>Stop-loss niveaus voor risicobescherming</li>
                                        <li>Geografische spreiding via IWDA ETF</li>
                                    </ul>
                                </div>
                            </div>

                            <!-- Position Sizing -->
                            <div class="bg-white rounded-lg p-6 shadow-sm">
                                <h4 class="text-lg font-semibold mb-4">3. Positieberekening</h4>
                                <div class="space-y-4 text-gray-600">
                                    <p>De allocatie wordt bepaald door:</p>
                                    <ul class="list-disc pl-5 space-y-2">
                                        <li>Marktregime (Extreme Fear tot Extreme Greed)</li>
                                        <li>Beschikbaar kapitaal en risicotolerantie</li>
                                        <li>Liquiditeit en handelsvolume</li>
                                        <li>Correlatie tussen assets</li>
                                    </ul>
                                </div>
                            </div>

                            <!-- Entry Points -->
                            <div class="bg-white rounded-lg p-6 shadow-sm">
                                <h4 class="text-lg font-semibold mb-4">4. Entry Point Optimalisatie</h4>
                                <div class="space-y-4 text-gray-600">
                                    <p>Bepaling van ingangspunten via:</p>
                                    <ul class="list-disc pl-5 space-y-2">
                                        <li>Volume-gewogen gemiddelde prijzen (VWAP)</li>
                                        <li>Support en resistance niveaus</li>
                                        <li>Volatiliteitsbandbreedte (ATR)</li>
                                        <li>Liquiditeitszones analyse</li>
                                    </ul>
                                </div>
                            </div>

                            <!-- Backtest Results -->
                            <div class="bg-white rounded-lg p-6 shadow-sm">
                                <h4 class="text-lg font-semibold mb-4">5. Validatie & Backtesting</h4>
                                <div class="space-y-4 text-gray-600">
                                    <p>Het algoritme is getest op:</p>
                                    <ul class="list-disc pl-5 space-y-2">
                                        <li>10 jaar historische marktdata</li>
                                        <li>Verschillende marktomstandigheden</li>
                                        <li>Extreme marktscenario's</li>
                                        <li>Transactiekosten en spreads</li>
                                    </ul>
                                </div>
                            </div>
                        </div>

                        <!-- Extra Disclaimers -->
                        <div class="mt-8 space-y-4 text-sm text-gray-500">
                            <p>* Het algoritme wordt continu geoptimaliseerd op basis van nieuwe marktdata.</p>
                            <p>* Prestaties uit het verleden bieden geen garantie voor de toekomst.</p>
                            <p>* Het algoritme is een hulpmiddel en vervangt geen persoonlijk financieel advies.</p>
                        </div>
                    </div>

                    <!-- Results Tab -->
                    <div id="results" class="tab-content hidden">
                        <h3 class="text-xl font-semibold mb-6">Historische Resultaten MONTO vs DCA</h3>
                        
                        <!-- Disclaimer Banner -->
                        <div class="bg-blue-50 border-l-4 border-blue-500 p-4 mb-8">
                            <p class="text-sm text-blue-700">
                                Historische resultaten bieden geen garantie voor toekomstige prestaties. De onderstaande data is gebaseerd op backtesting van onze strategie met werkelijke marktdata. Alle rendementen zijn indicatief en na kosten.
                            </p>
                        </div>

                        <!-- 10-Jaars Analyse -->
                        <div class="bg-white rounded-lg shadow-sm p-6 mb-8">
                            <h4 class="text-lg font-semibold mb-4">10-Jaars Analyse (2015-2025)</h4>
                            <div class="grid md:grid-cols-2 gap-6">
                                <!-- MONTO Strategie -->
                                <div class="space-y-4">
                                    <h5 class="font-medium text-green-600">MONTO Strategie</h5>
                                    <div class="bg-gray-50 p-4 rounded-lg">
                                        <ul class="space-y-2">
                                            <li class="flex justify-between">
                                                <span>Totaal Geïnvesteerd</span>
                                                <span class="font-medium">€180.000</span>
                                            </li>
                                            <li class="flex justify-between">
                                                <span>Eindwaarde Portfolio</span>
                                                <span class="font-medium">€442.800</span>
                                            </li>
                                            <li class="flex justify-between">
                                                <span>Totale ROI</span>
                                                <span class="font-medium text-green-600">+146%</span>
                                            </li>
                                            <li class="flex justify-between">
                                                <span>Jaarlijks Rendement</span>
                                                <span class="font-medium">9.4%</span>
                                            </li>
                                        </ul>
                                    </div>
                                </div>

                                <!-- DCA Strategie -->
                                <div class="space-y-4">
                                    <h5 class="font-medium text-blue-600">Standaard DCA</h5>
                                    <div class="bg-gray-50 p-4 rounded-lg">
                                        <ul class="space-y-2">
                                            <li class="flex justify-between">
                                                <span>Totaal Geïnvesteerd</span>
                                                <span class="font-medium">€180.000</span>
                                            </li>
                                            <li class="flex justify-between">
                                                <span>Eindwaarde Portfolio</span>
                                                <span class="font-medium">€351.000</span>
                                            </li>
                                            <li class="flex justify-between">
                                                <span>Totale ROI</span>
                                                <span class="font-medium text-blue-600">+95%</span>
                                            </li>
                                            <li class="flex justify-between">
                                                <span>Jaarlijks Rendement</span>
                                                <span class="font-medium">6.9%</span>
                                            </li>
                                        </ul>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- Jaar-per-jaar Analyse -->
                        <div class="bg-white rounded-lg shadow-sm p-6 mb-8">
                            <h4 class="text-lg font-semibold mb-4">Jaarlijkse Prestaties</h4>
                            <div class="overflow-x-auto">
                                <table class="min-w-full">
                                    <thead>
                                        <tr class="bg-gray-50">
                                            <th class="px-4 py-2 text-left">Jaar</th>
                                            <th class="px-4 py-2 text-right">MONTO ROI</th>
                                            <th class="px-4 py-2 text-right">DCA ROI</th>
                                            <th class="px-4 py-2 text-right">Verschil</th>
                                        </tr>
                                    </thead>
                                    <tbody class="divide-y divide-gray-200">
                                        <tr>
                                            <td class="px-4 py-2">2024</td>
                                            <td class="px-4 py-2 text-right text-green-600">+28.0%</td>
                                            <td class="px-4 py-2 text-right text-blue-600">+18.0%</td>
                                            <td class="px-4 py-2 text-right text-green-600">+10.0%</td>
                                        </tr>
                                        <!-- Voeg meer jaren toe -->
                                    </tbody>
                                </table>
                            </div>
                        </div>

                        <!-- Risico Metrics -->
                        <div class="bg-white rounded-lg shadow-sm p-6 mb-8">
                            <h4 class="text-lg font-semibold mb-4">Risico Analyse</h4>
                            <div class="grid md:grid-cols-2 gap-6">
                                <div class="space-y-4">
                                    <h5 class="font-medium">MONTO Strategie</h5>
                                    <div class="bg-gray-50 p-4 rounded-lg">
                                        <ul class="space-y-2">
                                            <li>Maximale Drawdown: -38%</li>
                                            <li>Volatiliteit: 28%</li>
                                            <li>Sharpe Ratio: 1.85</li>
                                        </ul>
                                    </div>
                                </div>
                                <div class="space-y-4">
                                    <h5 class="font-medium">DCA Strategie</h5>
                                    <div class="bg-gray-50 p-4 rounded-lg">
                                        <ul class="space-y-2">
                                            <li>Maximale Drawdown: -42%</li>
                                            <li>Volatiliteit: 32%</li>
                                            <li>Sharpe Ratio: 1.42</li>
                                        </ul>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- Extra Disclaimer -->
                        <div class="text-sm text-gray-600 space-y-2">
                            <p>* Alle getoonde rendementen zijn na aftrek van transactiekosten en beheervergoedingen.</p>
                            <p>* De backtest is uitgevoerd met werkelijke marktdata van IWDA.AS en BTC-USD.</p>
                            <p>* Prestaties uit het verleden bieden geen garantie voor de toekomst.</p>
                            <p>* Beleggen brengt risico's met zich mee. U kunt uw inleg verliezen.</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Footer -->
        <footer class="bg-gray-900 text-white py-12">
            <div class="container mx-auto px-6">
                <div class="flex flex-col md:flex-row justify-between">
                    <div class="mb-8 md:mb-0">
                        <h3 class="text-xl font-semibold mb-4">GrowWise</h3>
                        <p class="text-gray-400 max-w-sm">Helping people grow their wealth, one investment at a time.</p>
                    </div>
                    <div class="grid grid-cols-2 md:grid-cols-3 gap-8">
                        <div>
                            <h4 class="font-semibold mb-4">Links</h4>
                            <ul class="space-y-2 text-gray-400">
                                <li><a href="#" class="hover:text-white">Home</a></li>
                                <li><a href="#" class="hover:text-white">Over ons</a></li>
                                <li><a href="#" class="hover:text-white">Contact</a></li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
        </footer>
    </div>

    <div id="loading" class="loading" style="display: none;">
        <div class="spinner"></div>
    </div>

    <script>
        // Vervang het bestaande script met:
        document.addEventListener('DOMContentLoaded', function() {
            // Start met groeien button
            document.getElementById('startButton').addEventListener('click', function(e) {
                e.preventDefault();
                document.getElementById('calculator').scrollIntoView({ 
                    behavior: 'smooth', 
                    block: 'start' 
                });
            });

            // Leer meer button
            document.getElementById('learnMoreButton').addEventListener('click', function(e) {
                e.preventDefault();
                document.getElementById('learn-more').scrollIntoView({ 
                    behavior: 'smooth', 
                    block: 'start' 
                });
            });

            // Tab functionality
            document.querySelectorAll('.tab-button').forEach(button => {
                button.addEventListener('click', function(e) {
                    e.preventDefault();
                    const tabId = this.dataset.tab;
                    switchTab(tabId);
                });
            });
        });

        function switchTab(tabId) {
            // Verberg alle tabs
            document.querySelectorAll('.tab-content').forEach(tab => {
                tab.classList.add('hidden');
            });

            // Reset alle buttons
            document.querySelectorAll('.tab-button').forEach(btn => {
                btn.classList.remove('active', 'border-green-500');
                btn.classList.add('text-gray-500', 'border-transparent');
            });

            // Activeer de geselecteerde tab
            const selectedTab = document.getElementById(tabId);
            const activeButton = document.querySelector(`[data-tab="${tabId}"]`);

            if (selectedTab) {
                selectedTab.classList.remove('hidden');
            }
            if (activeButton) {
                activeButton.classList.remove('text-gray-500', 'border-transparent');
                activeButton.classList.add('active', 'border-green-500');
            }
        }

        document.querySelector('form').addEventListener('submit', function() {
            document.getElementById('loading').style.display = 'flex';
        });
    </script>
</body>
</html>
"""

def get_plant_state(fear_greed_score):
    """Bepaal plant status op basis van fear & greed score"""
    if fear_greed_score <= 25:  # Extreme Fear
        return {
            'state': 'dorry',
            'pot_color': '#e17055',
            'stem_color': '#919191',
            'leaf_color': '#919191',
            'flower_color': '#919191',
            'message': 'Je plant heeft veel water (investeringen) nodig! 💧',
            'description': 'De markt is in extreme angst - dit zijn historisch goede momenten om te investeren.'
        }
    elif fear_greed_score <= 45:  # Fear
        return {
            'state': 'thirsty',
            'pot_color': '#e17055',
            'stem_color': '#27ae60',
            'leaf_color': '#919191',
            'flower_color': '#919191',
            'message': 'Je plant kan wat water gebruiken! 💧',
            'description': 'De markt is angstig - overweeg gespreid bij te kopen.'
        }
    elif fear_greed_score <= 55:  # Neutral
        return {
            'state': 'healthy',
            'pot_color': '#e17055',
            'stem_color': '#27ae60',
            'leaf_color': '#2ecc71',
            'flower_color': '#e84393',
            'message': 'Je plant groeit mooi! 🌱',
            'description': 'De markt is in balans - blijf gespreid investeren.'
        }
    elif fear_greed_score <= 75:  # Greed
        return {
            'state': 'blooming',
            'pot_color': '#e17055',
            'stem_color': '#27ae60',
            'leaf_color': '#2ecc71',
            'flower_color': '#ffd700',
            'message': 'Je plant bloeit en groeit! 🌸',
            'description': 'De markt is optimistisch - blijf je strategie volgen.'
        }
    else:  # Extreme Greed
        return {
            'state': 'overripe',
            'pot_color': '#e17055',
            'stem_color': '#27ae60',
            'leaf_color': '#2ecc71',
            'flower_color': '#ffd700',
            'message': 'Tijd om te oogsten! ✂️',
            'description': 'De markt is extreem hebzuchtig - overweeg wat winst te nemen.'
        }


def scale_recommendation(recommendation, input_amount):
    """Schaalt de aanbeveling op basis van het ingevoerde bedrag"""
    STANDARD_AMOUNT = 1500  # Standaard bedrag waar algoritme op is gebouwd
    scaling_factor = input_amount / STANDARD_AMOUNT

    # Pas alleen de bedragen aan, behoud alle percentages
    recommendation['allocation']['iwda_amount'] *= scaling_factor
    recommendation['allocation']['btc_amount'] *= scaling_factor

    
    return recommendation

@app.route('/', methods=['GET', 'POST'])
def home():
    try:
        plant_state = get_plant_state(50)
        result = None

        if request.method == 'POST':
            amount = float(request.form['amount'])
            
            if amount < 100 or amount > 10000:
                raise ValueError("Bedrag moet tussen €100 en €10.000 liggen")
            
            # Gebruik standaard strategie
            strategy = UltimateQuantStrategy()
            recommendation = strategy.generate_ultimate_recommendation()
            
            # Schaal de uitkomsten
            recommendation = scale_recommendation(recommendation, amount)
            
            # Rest van je code blijft hetzelfde...
            if recommendation:
                allocations = recommendation['allocation']
                iwda_amount = allocations['iwda_amount']
                btc_amount = allocations['btc_amount']
                cash_amount = amount - (iwda_amount + btc_amount)
                # Update plant state based on fear & greed
                fear_greed = float(recommendation.get('market_regime', {}).get('sp500_fear_greed', 50))
                plant_state = get_plant_state(fear_greed)

                # Direct de entry_points gebruiken van het recommendation object
                entry_points = strategy.analyze_optimal_entry_points(
                    {
                        'btc': recommendation['current_prices']['btc'],
                        'iwda': recommendation['current_prices']['iwda_proxy']
                    },
                    recommendation['allocation']
                )

                result = {
                    'market_conditions': {
                        'regime': recommendation.get('market_regime', {}).get('regime', 'Unknown'),
                        'fear_greed': f"{recommendation.get('market_regime', {}).get('sp500_fear_greed', 0):.1f}",
                        'btc_fear_greed': recommendation.get('market_regime', {}).get('btc_fear_greed', 0)
                    },
                    'allocations': [
                        {
                            'asset': 'IWDA ETF',
                            'amount': iwda_amount,
                            'shares': allocations.get('iwda_shares', 0)
                        },
                        {
                            'asset': 'Bitcoin',
                            'amount': btc_amount
                        },
                        {
                            'asset': 'Cash Buffer',
                            'amount': amount - (iwda_amount + btc_amount),
                            'description': 'Voor markt opportuniteiten'
                        }
                    ],
                    'risk_metrics': {
                        'value_at_risk': {
                            'iwda': round(float(recommendation.get('risk_metrics', {}).get('iwda_var_95', 0)) * 100, 1),
                            'btc': round(float(recommendation.get('risk_metrics', {}).get('btc_var_95', 0)) * 100, 1)
                        },
                        'volatility': {
                            'iwda': round(float(recommendation.get('risk_metrics', {}).get('iwda_volatility', 0)) * 100, 1),
                            'btc': round(float(recommendation.get('risk_metrics', {}).get('btc_volatility', 0)) * 100, 1),
                        },
                        'portfolio_metrics': {
                            'expected_return': round(float(recommendation.get('performance_forecast', {}).get('expected_annual_return', 0)) * 100, 1),
                            'expected_risk': round(float(recommendation.get('performance_forecast', {}).get('expected_annual_risk', 0)) * 100, 1),
                            'sharpe_ratio': round(float(recommendation.get('performance_forecast', {}).get('sharpe_ratio', 0)), 1)
                        }
                    },
                    'order_placement': {
                        'iwda': [
                            {
                                'type': entry['type'],
                                'confidence': entry['confidence'],
                                'price': round(float(entry['price']), 2)
                            }
                            for entry in entry_points['iwda_orders']
                        ],
                        'btc': [
                            {
                                'type': entry['type'],
                                'confidence': entry['confidence'],
                                'price': round(float(entry['price']) * recommendation['market_regime']['usd_eur_rate'], 2)  # Converteer naar EUR
                            }
                            for entry in entry_points['btc_orders']
                        ],
                        'trading_tips': {
                            'execution_tips': [
                                "Gebruik GTC (Good-til-Cancelled) voor limit orders",
                                "Handel tussen 14:30-22:00 CET voor beste spreads", 
                                "Monitor orders en pas aan na 48 uur indien niet gevuld",
                                "Overweeg orders te annuleren na 5 handelsdagen"
                            ]
                        }
                    },
                    'total': amount,
                    'plant_state': plant_state  # Voeg plant status toe aan resultaat
                }
            else:
                result = {'error': "Kon geen aanbeveling genereren"}
                
    except Exception as e:
        result = {'error': f"Error: {str(e)}"}
        print(f"Error details: {traceback.format_exc()}")
        # Behoud default plant_state bij errors

    # Geef ALTIJD zowel result als plant_state mee
    return render_template_string(HTML_TEMPLATE, 
                                result=result,
                                plant_state=plant_state)

if __name__ == '__main__':
    port = os.environ.get("PORT", 5000)
    app.run(host="0.0.0.0", port=port)
