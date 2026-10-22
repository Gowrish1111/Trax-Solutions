from django.db import models


class Login(models.Model):
    login_id = models.AutoField(primary_key=True)

    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=128)

    ROLE_CHOICES = [
        ('student', 'Student'),
        ('trainer', 'Trainer'),
        ('admin', 'Admin'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    student = models.OneToOneField(
        'Student',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    trainer = models.OneToOneField(
        'Trainer',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.username

class Student(models.Model):
    student_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    age = models.IntegerField()
    dob = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Course(models.Model):
    course_id = models.AutoField(primary_key=True)

    course_name = models.CharField(max_length=100)

    description = models.TextField()

    fees = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    start_date = models.DateField()
    end_date = models.DateField()

    capacity = models.IntegerField(default=30)

    trainer = models.ForeignKey(
        'Trainer',
        on_delete=models.SET_NULL,
        null=True
    )

    def __str__(self):
        return self.course_name

    class Meta:
        ordering = ['course_name']


class Enrollment(models.Model):
    enrollment_id = models.AutoField(primary_key=True)
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE
    )
    enrollment_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.name} enrolled in {self.course.course_name}"


class Trainer(models.Model):
    Trainer_id = models.AutoField(primary_key=True)
    Trainer_name = models.CharField(max_length=50)
    email = models.EmailField()
    dept = models.CharField(max_length=100)

    def __str__(self):
        return self.Trainer_name


class Assessment(models.Model):
    assessment_id = models.AutoField(primary_key=True)
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    assessment_type = models.CharField(max_length=30)
    description = models.TextField()
    max_score = models.FloatField(default=100)
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.course.course_name})"

class Grade(models.Model):
    grade_id = models.AutoField(primary_key=True)
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE
    )
    assessment = models.ForeignKey(
        Assessment,
        on_delete=models.CASCADE
    )
    score = models.FloatField()

    def __str__(self):
        return f"{self.student.name} - {self.assessment.title} : {self.score}"