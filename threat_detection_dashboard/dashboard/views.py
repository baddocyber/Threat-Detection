from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import ThreatLog
from .email_utils import send_attack_email

@csrf_exempt
def save_threat(request):

    if request.method == "POST":

        data = json.loads(request.body)

        log = ThreatLog.objects.create(
            dur=data["dur"],
            proto=data["proto"],
            service=data["service"],
            state=data["state"],
            spkts=data["Spkts"],
            dpkts=data["Dpkts"],
            prediction=data["prediction"],
            threat_level=data["threat_level"]
        )

        # SEND EMAIL IF ATTACK
        if data["threat_level"] == "ATTACK":
            send_attack_email(data)

        return JsonResponse({"status": "saved", "id": log.id})

    return JsonResponse({"error": "invalid request"})

from django.http import JsonResponse
from .models import ThreatLog

def threat_stats(request):

    total = ThreatLog.objects.count()
    attacks = ThreatLog.objects.filter(threat_level="ATTACK").count()
    normal = ThreatLog.objects.filter(threat_level="NORMAL").count()

    return JsonResponse({
        "total": total,
        "attacks": attacks,
        "normal": normal
    })


def dashboard(request):
    return render(request, "dashboard.html")