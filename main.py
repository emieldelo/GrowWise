from flask import Flask, render_template, request, jsonify, abort, redirect, url_for, session
import jwt
import os

from MONTO_algorithm import UltimateQuantStrategy
import traceback

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "geheim")  # Nodig voor session




SUPABASE_JWT_SECRET = os.environ.get("JWT_SECRET")  # Haal de secret uit je environment

def verify_supabase_jwt(token):
    try:
        payload = jwt.decode(
            token,
            SUPABASE_JWT_SECRET,
            algorithms=["HS256"],
            options={"verify_aud": False}  # <-- voeg dit toe!
        )
        return payload
    except Exception as e:
        print(f"JWT verificatie mislukt: {e}")
        return None
    
def get_plant_state(fear_greed_score):
    """Bepaal plant status op basis van fear & greed score"""
    if fear_greed_score <= 25:  # Extreme Fear
        return {
            'state': 'dorry',
            'pot_color': "#583026",
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
            # AUTHENTICATIE CHECK
            auth_header = request.headers.get('Authorization', '')
            if not auth_header.startswith('Bearer '):
                abort(401)
            token = auth_header.split(' ')[1]
            if not verify_supabase_jwt(token):
                abort(401)

            amount = float(request.form['amount'])
            
            if amount <  100 or amount > 10000:
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

        # Sla resultaat tijdelijk op in de session
        session['result'] = result
        session['plant_state'] = plant_state
        return redirect(url_for('home'))

    # Geef ALTIJD zowel result als plant_state mee
    return render_template('home.html', result=result, plant_state=plant_state)

@app.errorhandler(401)
def unauthorized(e):
    if request.accept_mimetypes.accept_json:
        return jsonify({'error': 'Unauthorized'}), 401
    return render_template('401.html'), 401  # optioneel, als je een HTML pagina wilt

if __name__ == '__main__':
    app.debug = True  # Zet debug mode aan voor development
    app.run(host='0.0.0.0', port=8080)
