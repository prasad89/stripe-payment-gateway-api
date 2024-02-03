from flask import Flask, jsonify, request
import stripe
import os

app = Flask(__name__)

# Set the Stripe API key from the environment variable
stripe.api_key = os.getenv("STRIPE_API_KEY")


@app.route('/api/v1/create_intent', methods=['POST'])
def create_intent():
    """
    Endpoint to create a payment intent.
    """
    try:
        data = request.json
        amount = data['amount']
        currency = data['currency']
        automatic_payment_methods = data.get('automatic_payment_methods')

        # Create a payment intent using the Stripe API
        payment_intent = stripe.PaymentIntent.create(
            amount=amount,
            currency=currency,
            automatic_payment_methods=automatic_payment_methods
        )
        return jsonify({'clientSecret': payment_intent.client_secret})
    except stripe.error.StripeError as e:
        return jsonify(error=str(e)), 403


@app.route('/api/v1/capture_intent/<string:id>', methods=['POST'])
def capture_intent(id):
    """
    Endpoint to capture a payment intent.
    """
    try:
        # Capture the payment intent using the provided ID
        payment_intent = stripe.PaymentIntent.capture(
            id
        )
        return jsonify({'paymentIntent': payment_intent})
    except stripe.error.StripeError as e:
        return jsonify(error=str(e)), 403


@app.route('/api/v1/create_refund/<string:id>', methods=['POST'])
def create_refund(id):
    """
    Endpoint to create a refund for a payment.
    """
    try:
        # Create a refund for the provided charge ID
        refund = stripe.Refund.create(
            charge=id
        )
        return jsonify({'refund': refund})
    except stripe.error.StripeError as e:
        return jsonify(error=str(e)), 403   


@app.route('/api/v1/get_intents/', methods=['GET'])
def get_intents():
    """
    Endpoint to retrieve a list of payment intents.
    """
    try:
        # Retrieve a list of payment intents from Stripe
        intents = stripe.PaymentIntent.list()
        return jsonify({'intents': [intent.to_dict() for intent in intents]})
    except stripe.error.StripeError as e:
        return jsonify(error=str(e)), 403


if __name__ == "__main__":
    # Run the Flask app
    app.run(host='0.0.0.0', port=5000)