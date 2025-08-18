from django.urls import path
from api.views import JobList, LoginView, RegisterView, applyJobs, createJobPost, LogoutView


urlpatterns = [
    path('jobs/', JobList.as_view(), name = "job_list"),
    path('create_jobs/', createJobPost.as_view(), name = 'create_jobs'),
    path('get_candidates_applied/', createJobPost.as_view(), name ="cand_applied_jobs"),
    path('logout/', LogoutView.as_view(), name = 'logout'),
    path('apply/<int:pk>/', applyJobs.as_view(), name = "apply_job" ),
    path('get_applied_jobs/', applyJobs.as_view(), name  = 'get_applied_jobs'),
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
]
