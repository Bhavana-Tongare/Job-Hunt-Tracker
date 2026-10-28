
from database import create_tables, add_application, update_status

create_tables()

# Job 1: Applied -> Interview -> Rejected
job1 = add_application(
    company="ABC Technologies",
    job_title="Data Analyst",
    applied_date="2026-10-20",
    location="Pune",
    source="Naukri",
    salary_lpa=4.5,
)
update_status(job1, "Interview", "2026-10-25")
update_status(job1, "Rejected", "2026-10-27")

# Job 2: Applied only
job2 = add_application(
    company="XYZ Pvt Ltd",
    job_title="Python Developer",
    applied_date="2026-10-22",
    location="Nashik",
    source="LinkedIn",
    salary_lpa=4.0,
)

# Job 3: Applied -> Interview
job3 = add_application(
    company="Infosys",
    job_title="Python Developer",
    applied_date="2026-10-01",
    location="Pune",
    source="LinkedIn",
    salary_lpa=4.0,
)
update_status(job3, "Interview", "2026-10-10")

# Job 4: Applied only
job4 = add_application(
    company="TCS",
    job_title="Data Analyst",
    applied_date="2026-10-02",
    location="Pune",
    source="Naukri",
    salary_lpa=4.5,
)

# Job 5: Applied -> Assessment
job5 = add_application(
    company="Wipro",
    job_title="AI/ML Intern",
    applied_date="2026-10-04",
    location="Remote",
    source="Company Website",
    salary_lpa=3.0,
)
update_status(job5, "Assessment", "2026-10-12")

# Job 6: Applied -> Interview
job6 = add_application(
    company="Cognizant",
    job_title="Python Developer",
    applied_date="2026-10-05",
    location="Pune",
    source="Naukri",
    salary_lpa=4.0,
)
update_status(job6, "Interview", "2026-10-15")

# Job 7: Applied -> Offer
job7 = add_application(
    company="Persistent Systems",
    job_title="AI Engineer",
    applied_date="2026-10-07",
    location="Pune",
    source="LinkedIn",
    salary_lpa=6.0,
)
update_status(job7, "Interview", "2026-10-16")
update_status(job7, "Offer", "2026-10-24")

# Job 8: Applied -> Interview
job8 = add_application(
    company="Zensar Technologies",
    job_title="Data Scientist",
    applied_date="2026-10-08",
    location="Pune",
    source="Naukri",
    salary_lpa=5.5,
)
update_status(job8, "Interview", "2026-10-18")

# Job 9: Applied only
job9 = add_application(
    company="Tech Mahindra",
    job_title="GenAI Intern",
    applied_date="2026-10-09",
    location="Remote",
    source="LinkedIn",
    salary_lpa=3.5,
)

# Job 10: Applied -> Interview
job10 = add_application(
    company="IBM",
    job_title="Machine Learning Engineer",
    applied_date="2026-10-10",
    location="Bengaluru",
    source="Company Website",
    salary_lpa=7.0,
)
update_status(job10, "Interview", "2026-10-20")

# Job 11: Applied -> Assessment
job11 = add_application(
    company="Deloitte",
    job_title="Data Analyst",
    applied_date="2026-10-11",
    location="Pune",
    source="Referral",
    salary_lpa=5.0,
)
update_status(job11, "Assessment", "2026-10-19")

# Job 12: Applied only
job12 = add_application(
    company="Accenture",
    job_title="Python Developer",
    applied_date="2026-10-12",
    location="Mumbai",
    source="Naukri",
    salary_lpa=4.5,
)

# Job 13: Applied -> Interview
job13 = add_application(
    company="HCLTech",
    job_title="AI/ML Engineer",
    applied_date="2026-10-13",
    location="Pune",
    source="Indeed",
    salary_lpa=5.0,
)
update_status(job13, "Interview", "2026-10-22")

# Job 14: Applied -> Interview -> Rejected
job14 = add_application(
    company="LTIMindtree",
    job_title="Data Engineer",
    applied_date="2026-10-14",
    location="Pune",
    source="LinkedIn",
    salary_lpa=4.8,
)
update_status(job14, "Interview", "2026-10-21")
update_status(job14, "Rejected", "2026-10-26")

# Job 15: Applied only
job15 = add_application(
    company="Siemens",
    job_title="AI Engineer Trainee",
    applied_date="2026-10-15",
    location="Pune",
    source="Company Website",
    salary_lpa=5.5,
)

print("Sample job application data added successfully!")
