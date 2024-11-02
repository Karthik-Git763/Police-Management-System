from django.urls import path
from . import views

urlpatterns = [
    path("", views.home_police, name="policeHome"),
    path("login/", views.login_police, name="policeLogin"),
    path("logout/", views.logout_police, name="policeLogout"),
    path("selectCrime/", views.view_pending_crimes, name="pendingCrimes"),
    path("crimeDetail/<int:pk>", views.view_crime_details, name="crime"),
    path("cancelCrime/", views.cancel_current_crime, name="cancelCrime"),
    path("add_witness", views.add_witness, name="addWitness"),
    path("add_evidence/", views.add_evidence, name="addEvidence"),
    path("add_victim/", views.add_victim, name="addVictim"),
    path("add_suspect/", views.add_suspect, name="addSuspect"),
    path("evidence-list/", views.evidence_list, name="evidenceList"),
    path("addCriminal/", views.add_criminal, name="addCriminal"),
    path(
        "addCriminalToCrime",
        views.add_criminal_to_current_crime,
        name="addCriminalToCrime",
    ),
    path("viewCriminals", views.view_criminals, name="viewCriminals"),
    path("viewCriminals/<int:id>", views.criminal_details, name="criminalDetails"),
    path("witness/<int:pk>/", views.witness_detail, name="witnessDetail"),
    path("victim/<int:pk>/", views.victim_detail, name="victimDetail"),
    path("suspect/<int:pk>/", views.suspect_detail, name="suspectDetail"),
    path("evidence/<int:pk>/", views.evidence_detail, name="evidenceDetail"),
    path("updateWitness/<int:pk>", views.UpdateWitness.as_view(), name="updateWitness"),
    path("updateVictim/<int:pk>", views.UpdateVictim.as_view(), name="updateVictim"),
]
