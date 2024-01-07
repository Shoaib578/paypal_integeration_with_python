from flask import Flask, render_template, request
import paypalrestsdk

app = Flask(__name__)

# Set your PayPal credentials
paypalrestsdk.configure({
  "mode": "sandbox",  # Change to "live" for production
  "client_id": "AYM8fl3g_PnF-s3Uww4pHiDTQjjPiVQ3gpPk-VrwOieXZMU_kKRRv6E329gX5UZcDyC1VoiWghu2n0O3",
  "client_secret": "EBf4q-jFsk3yyIR_Ve0DwKCqHOFL00uZAsm7EpLztGDi7Z8LmtdKASJznkM9uTv0FWpDgKu2NQP6wNzq"
})

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create_payment', methods=['POST'])
def create_payment():
    amount = request.form['amount']
    # Create a PayPal payment
    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"
        },
        "transactions": [{
            "amount": {
                "total":amount,
                "currency": "USD"
            },
            "description": "Payment description"
        }],
        "redirect_urls": {
            "return_url": "http://localhost:5000/execute_payment",
            "cancel_url": "http://localhost:5000/cancel_payment"
        }
    })

    if payment.create():
        return render_template('redirect.html', url=payment.links[1].href)
    else:
        return 'Error while creating payment'

@app.route('/execute_payment', methods=['GET'])
def execute_payment():
    payment_id = request.args.get('paymentId')
    payer_id = request.args.get('PayerID')

    payment = paypalrestsdk.Payment.find(payment_id)

    if payment.execute({"payer_id": payer_id}):

        return render_template('success.html')
    else:
        return render_template('error.html')

@app.route('/cancel_payment')
def cancel_payment():
    return render_template('cancel.html')

if __name__ == '__main__':
    app.run(debug=True)
