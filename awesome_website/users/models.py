from django.db import models
import datetime
# Create your models here.





class employee_details(models.Model):
	full_name = models.CharField(max_length=150)
	mobile = models.CharField(max_length=150)
	role = models.CharField(max_length=150)
	status = models.CharField(max_length=50)
	def __str__(self):
		return self.full_name


class projects(models.Model):
	project_name = models.CharField(max_length=250)
	platform_name = models.CharField(max_length=250)
	open_status = models.CharField(max_length=100)
	close_status =models.CharField(max_length=100)

	def __str__(self):
		return self.project_name


class assignment(models.Model):
	employeeid = models.CharField(max_length=150)
	projectid = models.CharField(max_length=150)
	tl_id = models.CharField(max_length=150)
	first_work_done = models.CharField(max_length=50)
	date_from =models.CharField(max_length=150)
	from_to =models.CharField(max_length=150)

	def __str__(self):
		return self.employeeid

# class maintable(models.Model):
# 	fullname = models.CharField(max_length=150)
# 	mobile = models.CharField(max_length=150)
# 	projects = models.CharField(max_length=150)
# 	platform =models.CharField(max_length=150)
# 	created_date =models.CharField(max_length=150)

# 	def __str__(self):
# 		return self.fullname		



# users_employee_details
