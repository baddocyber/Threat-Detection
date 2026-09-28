from django.core.mail import send_mail

def send_attack_email(threat_data):

    subject = "🚨 TELECOM SECURITY ALERT - ATTACK DETECTED"

    message = f"""
    ALERT!

    A cyber attack has been detected in the telecom network.

    DETAILS:
    --------------------
    Duration: {threat_data['dur']}
    Protocol: {threat_data['proto']}
    Service: {threat_data['service']}
    State: {threat_data['state']}
    Packets Sent: {threat_data['spkts']}
    Packets Received: {threat_data['dpkts']}
    Threat Level: {threat_data['threat_level']}
    --------------------

    Immediate action recommended.
    """

    send_mail(
        subject,
        message,
        "adamarmiyau@gmail.com",
        ["adamarmiyau@gmail.com"],
        fail_silently=False
    )