from flask import Flask, request
import requests

app = Flask(__name__)

DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/XXXX/XXXX"  # replace with your webhook

@app.route("/paypal-ipn", methods=["POST"])
def paypal_ipn():
    # Validate IPN with PayPal
    verify_url = "https://ipnpb.paypal.com/cgi-bin/webscr"
    params = {"cmd": "_notify-validate"}
    params.update(request.form.to_dict())

    r = requests.post(verify_url, data=params)
    if r.text == "VERIFIED":
        payer = request.form.get("payer_email")
        amount = request.form.get("mc_gross")
        status = request.form.get("payment_status")

        requests.post(DISCORD_WEBHOOK_URL, json={
            "content": f"💰 Payment received!\nFrom: {payer}\nAmount: ${amount}\nStatus: {status}"
        })

    return "OK", 200
