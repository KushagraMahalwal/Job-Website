from api.models import job, User
from django.conf import settings
from rest_framework import status
from django.core.mail import send_mail
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from api.permissions import IsCandidate, IsRecruiter
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from api.serializers import JobSerializer, RegisterSerializer

# user register
class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"msg": "User registered successfully"}, status=200)
        return Response(serializer.errors, status=400)

# user login
class LoginView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        try:
            user_obj = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "Invalid email or password"}, status=401)

        user = authenticate(username=user_obj.username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            })
        return Response({"error": "Invalid email or password"}, status=401)

# user logout
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({"message": "Logout successful"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


# get all the jobs reruiter and candidates both can see
class JobList(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        all_jobs =  job.objects.all()
        serializer = JobSerializer(all_jobs, many = True)
        return Response(serializer.data, status = 200)
    
''' for candidate'''
# candidates apply for jobs
class applyJobs(APIView):
    permission_classes = [IsAuthenticated, IsCandidate]

    def post(self, request, pk):
        try:
            job_apply = job.objects.get(pk=pk)
        except job.DoesNotExist:
            return Response({'msg': 'No job found'}, status=404)

        # check if already applied
        if job_apply.apply_by.filter(id=request.user.id).exists():
            return Response({'msg': 'You have already applied to this job'}, status=400)

        # Add user to apply_by (ManyToManyField)
        job_apply.apply_by.add(request.user)
        job_apply.save()

        # Email to recruiter
        if job_apply.posted_by and job_apply.posted_by.email:
            send_mail(
                subject=f"New Application for {job_apply.title}",
                message=f"{request.user.username} has applied for your job: {job_apply.title}",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[job_apply.posted_by.email],
                fail_silently=False,
            )

        # Email to candidate
        if request.user.email:
            send_mail(
                subject=f"Application Submitted: {job_apply.title}",
                message=f"Hi {request.user.username},\n\nYou have successfully applied for the job '{job_apply.title}'.",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[request.user.email],
                fail_silently=False,
            )

        return Response({'msg': 'Job Applied'}, status=200)

    
    # applied jobs by a user
    def get(self, request):
        jobs = job.objects.filter(apply_by = request.user)
        if not jobs.exists():
            return Response({'msg':'No applied jobs'}, status = 400)
        serilizer = JobSerializer(jobs, many= True)
        return Response(serilizer.data, status = 200)

'''for recuiter'''
# creating the job
class createJobPost(APIView):
    permission_classes = [IsAuthenticated, IsRecruiter]
    def post(self, request):
        title = request.data.get('title')
        description = request.data.get('description')
        if not (title and description):
            return Response({'error':'please provide details'}, status = 400)
        
        jobcreate = job.objects.create(title = title, description = description, posted_by= request.user)
        return Response({'msg':'Job created successfully'},status = 200)

    # jobs posted  by the recuiter and apply by user is not null
    def get(self, request):
        all_app = job.objects.filter(posted_by = request.user).distinct() 
        if not all_app.exists():
            return Response({'msg':'No canditate applied for this job'})
        serializer = JobSerializer(all_app, many = True)
        return Response(serializer.data, status = 200)
    



