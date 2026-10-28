import sqlite3
import pandas as pd
import streamlit as st

from database import (
    STATUSES, create_tables, get_connection, add_application, update_status,
)

create_tables()

st.set_page_config(
    page_title="Job Hunt Tracker",
    page_icon="💼",
    layout="wide",
)

JOB_TYPES = ["Full-time", "Internship", "Part-time", "Contract"]
SOURCES = ["Naukri", "LinkedIn", "Company Website", "Indeed", "Referral", "Other"]
STATUS_ICONS = {
    "Applied": "📨", "Assessment": "📝", "Interview": "🎤", "Offer": "🎉",
    "Rejected": "❌", "Withdrawn": "↩️", "No Response": "⏳",
}

# ---------- THEME ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');

:root {
    --primary: #6C5CE7;
    --primary-dark: #5846D6;
    --ink: #1F2A44;
    --muted: #64748B;
    --border: #AEBBD3;
}

.stApp {
    background: linear-gradient(135deg, #EEF4FF 0%, #F6F2FF 100%);
    color: var(--ink);
    font-family: 'Poppins', sans-serif;
}
input, textarea, button { font-family: 'Poppins', sans-serif !important; }

[data-testid="stHeader"] { background: transparent; }

.block-container {
    max-width: 1200px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* ---------- Hero ---------- */
.hero {
    position: relative;
    overflow: hidden;
    background: linear-gradient(120deg, #6C5CE7 0%, #8E7CFF 55%, #5B8DEF 100%);
    border-radius: 24px;
    padding: 34px 38px;
    margin-bottom: 26px;
    box-shadow: 0 14px 34px rgba(108, 92, 231, 0.28);
}
.hero::after {
    content: "";
    position: absolute;
    right: -50px; top: -60px;
    width: 230px; height: 230px;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.13);
}
.hero-tag {
    display: inline-block;
    background: #FFFFFF;
    color: var(--primary);
    padding: 6px 14px;
    border-radius: 30px;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 1px;
    margin-bottom: 14px;
}
.hero h1 {
    color: #FFFFFF !important;
    font-size: 36px;
    font-weight: 700;
    margin: 0 0 10px 0;
    padding: 0 !important;
}
.hero p {
    color: rgba(255, 255, 255, 0.88);
    font-size: 15px;
    margin: 0;
    line-height: 1.7;
    max-width: 640px;
}

/* ---------- Headings and labels ---------- */
h2, h3, h4, h5 { color: var(--ink) !important; font-weight: 700 !important; }
[data-testid="stWidgetLabel"] p { color: #475775 !important; font-size: 14px !important; font-weight: 500; }

/* ---------- Tabs ---------- */
.stTabs [data-baseweb="tab-list"] { gap: 8px; border-bottom: 2px solid #DCE3F2; }
.stTabs [data-baseweb="tab"] { font-weight: 600; color: var(--muted); padding: 10px 18px; }
.stTabs [aria-selected="true"] { color: var(--primary) !important; }
.stTabs [data-baseweb="tab-highlight"] { background-color: var(--primary) !important; }

/* ---------- Form card ---------- */
[data-testid="stForm"] {
    background: #FFFFFF;
    border: 1.5px solid #C9D3E6;
    border-radius: 20px;
    padding: 28px;
    box-shadow: 0 10px 32px rgba(63, 85, 140, 0.08);
}

/* ---------- Input boxes (visible fill + border) ---------- */
.stApp [data-baseweb="input"],
.stApp [data-baseweb="textarea"],
.stApp [data-baseweb="select"] > div {
    background-color: #F4F6FC !important;
    border: 2px solid #9FB0CE !important;
    border-radius: 10px !important;
    box-shadow: none !important;
    transition: border-color 0.15s ease, box-shadow 0.15s ease;
}
.stApp [data-baseweb="base-input"] {
    background-color: transparent !important;
    border: none !important;
}
.stApp [data-baseweb="input"] input,
.stApp [data-baseweb="textarea"] textarea {
    background-color: transparent !important;
    border: none !important;
    box-shadow: none !important;
    color: var(--ink) !important;
}
::placeholder { color: #94A3B8 !important; opacity: 1 !important; }

/* Hover and focus: the box lights up so users know where to click */
.stApp [data-baseweb="input"]:hover,
.stApp [data-baseweb="textarea"]:hover,
.stApp [data-baseweb="select"] > div:hover {
    border-color: #6C5CE7 !important;
}
.stApp [data-baseweb="input"]:focus-within,
.stApp [data-baseweb="textarea"]:focus-within,
.stApp [data-baseweb="select"] > div:focus-within {
    background-color: #FFFFFF !important;
    border-color: #6C5CE7 !important;
    box-shadow: 0 0 0 3px rgba(108, 92, 231, 0.18) !important;
}

/* Hide the small "Press Enter to submit form" hint */
[data-testid="InputInstructions"] { display: none !important; }

/* Dropdown text and options */
[data-baseweb="select"] span { color: var(--ink) !important; }
[data-baseweb="popover"], [data-baseweb="menu"] { background: #FFFFFF !important; }
[role="option"] { background: #FFFFFF !important; color: var(--ink) !important; }
[role="option"]:hover, [role="option"][aria-selected="true"] { background: #EEEAFE !important; }

/* Multiselect tags */
[data-baseweb="tag"] { background: var(--primary) !important; border-radius: 8px !important; }
[data-baseweb="tag"] span { color: #FFFFFF !important; }

/* Number input +/- buttons */
.stNumberInput button {
    background: #F3F0FF !important;
    color: #475775 !important;
    border: none !important;
}

/* ---------- Save button (centred) ---------- */
.stFormSubmitButton,
[data-testid="stFormSubmitButton"] {
    display: flex !important;
    justify-content: center !important;
    width: 100% !important;
}
.stFormSubmitButton button,
[data-testid="stFormSubmitButton"] button {
    min-width: 260px;
    background: linear-gradient(100deg, #6C5CE7, #5B8DEF) !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 10px !important;
    min-height: 46px !important;
    font-size: 15px !important;
    font-weight: 600 !important;
    box-shadow: 0 6px 16px rgba(108, 92, 231, 0.3);
    transition: transform 0.15s ease, box-shadow 0.15s ease;
}
.stFormSubmitButton button:hover,
[data-testid="stFormSubmitButton"] button:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 22px rgba(108, 92, 231, 0.38);
    color: #FFFFFF !important;
}

/* ---------- KPI cards ---------- */
[data-testid="stMetric"] {
    background: #FFFFFF !important;
    padding: 16px 20px;
    border: 1px solid #DCE3F2 !important;
    border-left: 5px solid var(--primary) !important;
    border-radius: 14px !important;
    box-shadow: 0 4px 16px rgba(63, 85, 140, 0.07);
    transition: transform 0.15s ease, box-shadow 0.15s ease;
}
[data-testid="stMetric"]:hover {
    transform: translateY(-3px);
    box-shadow: 0 10px 24px rgba(63, 85, 140, 0.13);
}
[data-testid="stMetricLabel"] p { color: var(--muted) !important; font-weight: 500; }
[data-testid="stMetricValue"] { color: var(--primary) !important; font-weight: 700; }

/* ---------- Table and messages ---------- */
[data-testid="stDataFrame"] {
    border: 1px solid #DCE3F2 !important;
    border-radius: 14px !important;
    overflow: hidden;
    box-shadow: 0 4px 16px rgba(63, 85, 140, 0.06);
}
[data-testid="stAlert"] { border-radius: 12px; }
hr { border-color: #DCE3F2; margin: 24px 0; }

/* ---------- Mobile ---------- */
@media (max-width: 768px) {
    .hero { padding: 22px; }
    .hero h1 { font-size: 27px; }
    [data-testid="stForm"] { padding: 16px; }
}
</style>
""", unsafe_allow_html=True)


# ---------- DATA HELPERS ----------
def load_kpis():
    """Counts use the events table, so an application that reached
    'Interview' and was rejected later still counts as an interview."""
    with get_connection() as conn:
        total = conn.execute("SELECT COUNT(*) FROM applications").fetchone()[0]
        interviews = conn.execute(
            """SELECT COUNT(DISTINCT application_id)
               FROM application_events WHERE status = 'Interview'"""
        ).fetchone()[0]
        offers = conn.execute(
            """SELECT COUNT(DISTINCT application_id)
               FROM application_events WHERE status = 'Offer'"""
        ).fetchone()[0]
    return total, interviews, offers


def load_applications():
    with get_connection() as conn:
        return pd.read_sql_query(
            """SELECT id, company, job_title, applied_date, location, job_type,
                      source, status, salary_lpa, job_url, notes
               FROM applications
               ORDER BY applied_date DESC, id DESC""",
            conn,
        )


# ---------- HEADER ----------
st.markdown("""
<div class="hero">
    <div class="hero-tag">✦ YOUR CAREER JOURNEY</div>
    <h1>💼 Job Hunt Tracker</h1>
    <p>
        Your next opportunity starts here. Organize your applications,
        keep track of every opportunity, and stay focused on your goals.
    </p>
</div>
""", unsafe_allow_html=True)

# One-time success message shown after a save
flash = st.session_state.pop("flash", None)
if flash:
    st.success(flash)

# ---------- KPI CARDS ----------
try:
    total, interviews, offers = load_kpis()
    rate = (interviews / total * 100) if total else 0

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("📨 Total Applications", total)
    k2.metric(
        "🎤 Reached Interview", interviews,
        help="Counts every application that ever reached the interview "
             "stage, even if it was rejected later.",
    )
    k3.metric("🎉 Offers", offers)
    k4.metric("📈 Interview Rate", f"{rate:.0f}%")
except sqlite3.Error as error:
    st.error(f"Could not load summary numbers: {error}")

st.write("")

# Changing this number gives the form a new identity, which resets it
if "form_version" not in st.session_state:
    st.session_state.form_version = 0

tab_add, tab_list = st.tabs(["✦ Add Application", "📋 My Applications"])

# ---------- TAB 1: ADD APPLICATION ----------
with tab_add:
    st.caption("Company name and job title are required.")

    with st.form(f"job_form_{st.session_state.form_version}"):
        st.markdown("##### 🏢 Job Information")
        col1, col2 = st.columns(2, gap="large")

        with col1:
            company = st.text_input("Company Name *", placeholder="e.g. Google")
            job_title = st.text_input("Job Title *", placeholder="e.g. Data Analyst")
            location = st.text_input("Location", placeholder="e.g. Pune, Maharashtra")
            applied_date = st.date_input("Application Date")

        with col2:
            job_type = st.selectbox("Job Type", JOB_TYPES)
            source = st.selectbox("Where did you find this job?", SOURCES)
            status = st.selectbox("Application Status", STATUSES)
            salary_lpa = st.number_input(
                "Expected Salary (LPA)",
                min_value=0.0, value=0.0, step=0.5,
                help="Enter 0 if the salary is not known.",
            )

        st.divider()
        st.markdown("##### 🔗 Links & Notes")

        job_url = st.text_input(
            "Job Posting URL", placeholder="Paste the job posting link here"
        )
        notes = st.text_area(
            "Notes",
            placeholder="Recruiter details, interview date, next steps...",
            height=100,
        )

        st.write("")
        _, button_col, _ = st.columns([2, 2, 2])
        with button_col:
            submitted = st.form_submit_button("Save Application")

    if submitted:
        if not company.strip() or not job_title.strip():
            st.error("Please enter both the company name and job title.")
        else:
            saved = False
            try:
                app_id = add_application(
                    company=company.strip(),
                    job_title=job_title.strip(),
                    applied_date=applied_date.isoformat(),
                    location=location.strip() or None,
                    job_type=job_type,
                    source=source,
                    salary_lpa=salary_lpa if salary_lpa > 0 else None,
                    job_url=job_url.strip() or None,
                    notes=notes.strip() or None,
                )
                # add_application() always logs "Applied" first.
                # If you picked another status, log that change too.
                if status != "Applied":
                    update_status(app_id, status)
                saved = True
            except (sqlite3.Error, ValueError) as error:
                st.error(f"Could not save the application: {error}")

            if saved:
                st.session_state.flash = (
                    f"🎉 Application at {company.strip()} saved successfully!"
                )
                st.session_state.form_version += 1
                st.rerun()

# ---------- TAB 2: SAVED APPLICATIONS ----------
with tab_list:
    try:
        df = load_applications()

        if df.empty:
            st.info(
                "🌱 Your application list is empty. "
                "Add your first opportunity in the first tab."
            )
        else:
            selected = st.multiselect(
                "Filter by status", STATUSES, default=STATUSES
            )
            view = df[df["status"].isin(selected)].copy()
            st.caption(f"Showing {len(view)} of {len(df)} applications")

            view["applied_date"] = pd.to_datetime(view["applied_date"], errors="coerce")
            view["status"] = view["status"].map(
                lambda s: f"{STATUS_ICONS.get(s, '•')} {s}"
            )

            st.dataframe(
                view,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "id": st.column_config.NumberColumn("ID", width="small"),
                    "company": "Company",
                    "job_title": "Job Title",
                    "applied_date": st.column_config.DateColumn(
                        "Applied On", format="DD MMM YYYY"
                    ),
                    "location": "Location",
                    "job_type": "Type",
                    "source": "Source",
                    "status": "Status",
                    "salary_lpa": st.column_config.NumberColumn(
                        "Salary (LPA)", format="%.1f"
                    ),
                    "job_url": st.column_config.LinkColumn(
                        "Job Link", display_text="Open ↗"
                    ),
                    "notes": "Notes",
                },
            )

    except (sqlite3.Error, pd.errors.DatabaseError) as error:
        st.error(f"Could not load saved applications: {error}")

# ---------- FOOTER ----------
st.markdown("""
<div style="text-align:center; color:#8190AA; font-size:12px; padding:28px 0 8px 0;">
    Made with 💜 for your next career opportunity
</div>
""", unsafe_allow_html=True)