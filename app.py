import sqlite3

import altair as alt
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
STATUS_COLORS = {
    "Applied": "#6C5CE7", "Assessment": "#5B8DEF", "Interview": "#00B8D9",
    "Offer": "#22C55E", "Rejected": "#F43F5E", "Withdrawn": "#94A3B8",
    "No Response": "#F59E0B",
}
FUNNEL_STAGES = ["Applied", "Assessment", "Interview", "Offer"]

PURPLE, BLUE, SOFT = "#6C5CE7", "#5B8DEF", "#D9D3FB"

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

.block-container { max-width: 1200px; padding-top: 2rem; padding-bottom: 3rem; }

/* ---------- Hero ---------- */
.hero {
    position: relative; overflow: hidden;
    background: linear-gradient(120deg, #6C5CE7 0%, #8E7CFF 55%, #5B8DEF 100%);
    border-radius: 24px; padding: 34px 38px; margin-bottom: 26px;
    box-shadow: 0 14px 34px rgba(108, 92, 231, 0.28);
}
.hero::after {
    content: ""; position: absolute; right: -50px; top: -60px;
    width: 230px; height: 230px; border-radius: 50%;
    background: rgba(255, 255, 255, 0.13);
}
.hero-tag {
    display: inline-block; background: #FFFFFF; color: var(--primary);
    padding: 6px 14px; border-radius: 30px; font-size: 12px;
    font-weight: 700; letter-spacing: 1px; margin-bottom: 14px;
}
.hero h1 {
    color: #FFFFFF !important; font-size: 36px; font-weight: 700;
    margin: 0 0 10px 0; padding: 0 !important;
}
.hero p {
    color: rgba(255, 255, 255, 0.88); font-size: 15px; margin: 0;
    line-height: 1.7; max-width: 640px;
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
    background: #FFFFFF; border: 1.5px solid #C9D3E6; border-radius: 20px;
    padding: 28px; box-shadow: 0 10px 32px rgba(63, 85, 140, 0.08);
}

/* ---------- Input boxes ---------- */
.stApp [data-baseweb="input"],
.stApp [data-baseweb="textarea"],
.stApp [data-baseweb="select"] > div {
    background-color: #F4F6FC !important; border: 2px solid #9FB0CE !important;
    border-radius: 10px !important; box-shadow: none !important;
    transition: border-color 0.15s ease, box-shadow 0.15s ease;
}
.stApp [data-baseweb="base-input"] { background-color: transparent !important; border: none !important; }
.stApp [data-baseweb="input"] input,
.stApp [data-baseweb="textarea"] textarea {
    background-color: transparent !important; border: none !important;
    box-shadow: none !important; color: var(--ink) !important;
}
::placeholder { color: #94A3B8 !important; opacity: 1 !important; }
.stApp [data-baseweb="input"]:hover,
.stApp [data-baseweb="textarea"]:hover,
.stApp [data-baseweb="select"] > div:hover { border-color: #6C5CE7 !important; }
.stApp [data-baseweb="input"]:focus-within,
.stApp [data-baseweb="textarea"]:focus-within,
.stApp [data-baseweb="select"] > div:focus-within {
    background-color: #FFFFFF !important; border-color: #6C5CE7 !important;
    box-shadow: 0 0 0 3px rgba(108, 92, 231, 0.18) !important;
}
[data-testid="InputInstructions"] { display: none !important; }
[data-baseweb="select"] span { color: var(--ink) !important; }
[data-baseweb="popover"], [data-baseweb="menu"] { background: #FFFFFF !important; }
[role="option"] { background: #FFFFFF !important; color: var(--ink) !important; }
[role="option"]:hover, [role="option"][aria-selected="true"] { background: #EEEAFE !important; }
[data-baseweb="tag"] { background: var(--primary) !important; border-radius: 8px !important; }
[data-baseweb="tag"] span { color: #FFFFFF !important; }
.stNumberInput button { background: #F3F0FF !important; color: #475775 !important; border: none !important; }

/* ---------- Save button ---------- */
.stFormSubmitButton, [data-testid="stFormSubmitButton"] {
    display: flex !important; justify-content: center !important; width: 100% !important;
}
.stFormSubmitButton button, [data-testid="stFormSubmitButton"] button {
    min-width: 260px; background: linear-gradient(100deg, #6C5CE7, #5B8DEF) !important;
    color: #FFFFFF !important; border: none !important; border-radius: 10px !important;
    min-height: 46px !important; font-size: 15px !important; font-weight: 600 !important;
    box-shadow: 0 6px 16px rgba(108, 92, 231, 0.3);
    transition: transform 0.15s ease, box-shadow 0.15s ease;
}
.stFormSubmitButton button:hover, [data-testid="stFormSubmitButton"] button:hover {
    transform: translateY(-2px); box-shadow: 0 10px 22px rgba(108, 92, 231, 0.38);
    color: #FFFFFF !important;
}

/* ---------- KPI cards ---------- */
[data-testid="stMetric"] {
    background: #FFFFFF !important; padding: 16px 20px;
    border: 1px solid #DCE3F2 !important; border-left: 5px solid var(--primary) !important;
    border-radius: 14px !important; box-shadow: 0 4px 16px rgba(63, 85, 140, 0.07);
}
[data-testid="stMetricLabel"] p { color: var(--muted) !important; font-weight: 500; }
[data-testid="stMetricValue"] { color: var(--primary) !important; font-weight: 700; }

/* ---------- Chart cards (st.container(border=True)) ---------- */
[data-testid="stVerticalBlockBorderWrapper"] {
    background: #FFFFFF; border: 1px solid #DCE3F2 !important;
    border-radius: 18px !important; padding: 8px 10px;
    box-shadow: 0 4px 18px rgba(63, 85, 140, 0.07);
}
.chart-title { font-size: 16px; font-weight: 700; color: var(--ink); margin: 6px 0 0 0; }
.chart-sub { font-size: 12.5px; color: var(--muted); margin: 0 0 6px 0; }

/* ---------- Insight cards ---------- */
.insight {
    height: 100%; border-radius: 18px; padding: 20px 22px; color: #FFFFFF;
    box-shadow: 0 10px 26px rgba(63, 85, 140, 0.18);
}
.insight.a { background: linear-gradient(120deg, #6C5CE7, #8E7CFF); }
.insight.b { background: linear-gradient(120deg, #3B82F6, #5B8DEF); }
.insight.c { background: linear-gradient(120deg, #0EA5A4, #22C1C3); }
.insight .label { font-size: 12.5px; opacity: .9; font-weight: 500; }
.insight .value { font-size: 24px; font-weight: 700; margin: 4px 0 2px 0; line-height: 1.25; }
.insight .sub { font-size: 12.5px; opacity: .9; }

/* ---------- Table and messages ---------- */
[data-testid="stDataFrame"] {
    border: 1px solid #DCE3F2 !important; border-radius: 14px !important;
    overflow: hidden; box-shadow: 0 4px 16px rgba(63, 85, 140, 0.06);
}
[data-testid="stAlert"] { border-radius: 12px; }
hr { border-color: #DCE3F2; margin: 24px 0; }

@media (max-width: 768px) {
    .hero { padding: 22px; }
    .hero h1 { font-size: 27px; }
    [data-testid="stForm"] { padding: 16px; }
}
</style>
""", unsafe_allow_html=True)


# ---------- CHART HELPERS ----------
def style_chart(chart, height=300):
    """Apply one consistent look to every Altair chart."""
    return (
        chart.properties(height=height)
        .configure(background="transparent", font="Poppins")
        .configure_view(strokeWidth=0)
        .configure_axis(
            labelColor="#64748B", titleColor="#64748B", labelFontSize=12,
            titleFontSize=12, grid=True, gridColor="#EEF1F8", domain=False,
            tickSize=0,
        )
        .configure_legend(labelColor="#475775", titleColor="#475775", orient="bottom")
    )


def card_header(title, subtitle):
    st.markdown(
        f'<p class="chart-title">{title}</p><p class="chart-sub">{subtitle}</p>',
        unsafe_allow_html=True,
    )


def insight_card(css_class, label, value, sub):
    st.markdown(
        f'<div class="insight {css_class}"><div class="label">{label}</div>'
        f'<div class="value">{value}</div><div class="sub">{sub}</div></div>',
        unsafe_allow_html=True,
    )


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


def load_platform_stats(conn):
    return pd.read_sql_query(
        """
        SELECT
            COALESCE(NULLIF(TRIM(a.source), ''), 'Unknown') AS Platform,
            COUNT(DISTINCT a.id) AS Applications,
            COUNT(DISTINCT CASE WHEN e.status = 'Interview' THEN a.id END) AS Interviews,
            COUNT(DISTINCT CASE WHEN e.status = 'Offer' THEN a.id END) AS Offers
        FROM applications a
        LEFT JOIN application_events e ON e.application_id = a.id
        GROUP BY COALESCE(NULLIF(TRIM(a.source), ''), 'Unknown')
        """,
        conn,
    )


def load_funnel(conn):
    df = pd.read_sql_query(
        """SELECT status, COUNT(DISTINCT application_id) AS Count
           FROM application_events GROUP BY status""",
        conn,
    )
    counts = dict(zip(df["status"], df["Count"]))
    return pd.DataFrame(
        {"Stage": FUNNEL_STAGES, "Count": [int(counts.get(s, 0)) for s in FUNNEL_STAGES]}
    )


def load_title_stats(conn):
    return pd.read_sql_query(
        """
        SELECT a.job_title AS "Job Title",
               COUNT(DISTINCT a.id) AS Applications,
               COUNT(DISTINCT CASE WHEN e.status = 'Interview' THEN a.id END) AS Interviews
        FROM applications a
        LEFT JOIN application_events e ON e.application_id = a.id
        GROUP BY a.job_title
        HAVING Interviews > 0
        ORDER BY Interviews DESC, Applications DESC
        LIMIT 8
        """,
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

if "form_version" not in st.session_state:
    st.session_state.form_version = 0

tab_dash, tab_add, tab_list = st.tabs(
    ["📊 Analytics", "✦ Add Application", "📋 My Applications"]
)

# ---------- TAB 1: ANALYTICS ----------
with tab_dash:
    try:
        with get_connection() as conn:
            platform_df = load_platform_stats(conn)
            funnel_df = load_funnel(conn)
            title_df = load_title_stats(conn)
        apps_df = load_applications()
    except (sqlite3.Error, pd.errors.DatabaseError) as error:
        st.error(f"Could not load analytics: {error}")
        platform_df = pd.DataFrame()
        funnel_df = pd.DataFrame()
        title_df = pd.DataFrame()
        apps_df = pd.DataFrame()

    if platform_df.empty or apps_df.empty:
        st.info("🌱 Add a few applications to unlock your analytics.")
    else:
        platform_df["Interview Rate (%)"] = (
            platform_df["Interviews"] / platform_df["Applications"] * 100
        ).round(1)

        # ----- Insight cards -----
        top = platform_df.sort_values(
            ["Interviews", "Applications"], ascending=False
        ).iloc[0]
        with_interviews = platform_df[platform_df["Interviews"] > 0]

        c1, c2, c3 = st.columns(3, gap="medium")
        with c1:
            if top["Interviews"] > 0:
                insight_card("a", "🏆 Most interviews from", top["Platform"],
                             f'{int(top["Interviews"])} interview(s) from '
                             f'{int(top["Applications"])} applications')
            else:
                insight_card("a", "🏆 Most interviews from", "No data yet",
                             "Interviews will appear here")
        with c2:
            if not with_interviews.empty:
                best = with_interviews.sort_values(
                    ["Interview Rate (%)", "Interviews"], ascending=False
                ).iloc[0]
                insight_card("b", "🎯 Best interview rate", best["Platform"],
                             f'{best["Interview Rate (%)"]:.1f}% '
                             f'({int(best["Interviews"])}/{int(best["Applications"])})')
            else:
                insight_card("b", "🎯 Best interview rate", "No data yet",
                             "Record an interview to see this")
        with c3:
            if not title_df.empty:
                t = title_df.iloc[0]
                insight_card("c", "💡 Top job title", t["Job Title"],
                             f'{int(t["Interviews"])} interview(s)')
            else:
                insight_card("c", "💡 Top job title", "No data yet",
                             "Record an interview to see this")

        st.write("")

        # ----- Funnel + status donut -----
        left, right = st.columns([3, 2], gap="medium")

        with left:
            with st.container(border=True):
                card_header("Application funnel",
                            "How far your applications travel. Rejected ones still count.")
                base = funnel_df["Count"].iloc[0] or 1
                funnel_df["Share"] = (funnel_df["Count"] / base * 100).round(0)
                funnel_df["Label"] = funnel_df.apply(
                    lambda r: f'{r["Count"]}  ({int(r["Share"])}%)', axis=1
                )
                bars = alt.Chart(funnel_df).mark_bar(
                    cornerRadiusTopRight=8, cornerRadiusBottomRight=8, size=34
                ).encode(
                    y=alt.Y("Stage:N", sort=FUNNEL_STAGES, title=None),
                    x=alt.X("Count:Q", title=None,
                            scale=alt.Scale(domain=[0, max(base, 1) * 1.25])),
                    color=alt.Color(
                        "Stage:N", legend=None,
                        scale=alt.Scale(
                            domain=FUNNEL_STAGES,
                            range=[STATUS_COLORS[s] for s in FUNNEL_STAGES],
                        ),
                    ),
                    tooltip=["Stage", "Count", "Share"],
                )
                labels = alt.Chart(funnel_df).mark_text(
                    align="left", dx=6, fontSize=12, fontWeight=600, color="#1F2A44"
                ).encode(
                    y=alt.Y("Stage:N", sort=FUNNEL_STAGES),
                    x="Count:Q", text="Label:N",
                )
                st.altair_chart(style_chart(bars + labels, 260),
                                width="stretch")

        with right:
            with st.container(border=True):
                card_header("Where things stand", "Current status of all applications")
                status_df = (
                    apps_df["status"].value_counts().rename_axis("Status")
                    .reset_index(name="Count")
                )
                donut = alt.Chart(status_df).mark_arc(
                    innerRadius=62, outerRadius=105, cornerRadius=5, padAngle=0.02
                ).encode(
                    theta="Count:Q",
                    color=alt.Color(
                        "Status:N",
                        scale=alt.Scale(
                            domain=list(STATUS_COLORS),
                            range=list(STATUS_COLORS.values()),
                        ),
                    ),
                    tooltip=["Status", "Count"],
                )
                st.altair_chart(style_chart(donut, 260), width="stretch")

        # ----- Platform comparison -----
        with st.container(border=True):
            card_header("Job platforms compared",
                        "Light bar = applications sent, dark bar = interviews received")
            order = platform_df.sort_values("Applications", ascending=False)["Platform"].tolist()
            apps_bar = alt.Chart(platform_df).mark_bar(
                color=SOFT, cornerRadiusTopRight=8, cornerRadiusBottomRight=8, size=30
            ).encode(
                y=alt.Y("Platform:N", sort=order, title=None),
                x=alt.X("Applications:Q", title=None),
                tooltip=["Platform", "Applications", "Interviews",
                         alt.Tooltip("Interview Rate (%):Q", format=".1f")],
            )
            int_bar = alt.Chart(platform_df).mark_bar(
                color=PURPLE, cornerRadiusTopRight=6, cornerRadiusBottomRight=6, size=14
            ).encode(
                y=alt.Y("Platform:N", sort=order),
                x="Interviews:Q",
            )
            app_text = alt.Chart(platform_df).mark_text(
                align="left", dx=6, fontSize=12, color="#64748B"
            ).encode(
                y=alt.Y("Platform:N", sort=order), x="Applications:Q",
                text=alt.Text("Applications:Q"),
            )
            st.altair_chart(
                style_chart(apps_bar + int_bar + app_text, 40 + 46 * len(platform_df)),
                width="stretch",
            )

            table_df = platform_df.sort_values(
                ["Interview Rate (%)", "Interviews"], ascending=False
            )[["Platform", "Applications", "Interviews", "Offers", "Interview Rate (%)"]]
            st.dataframe(
                table_df, width="stretch", hide_index=True,
                column_config={
                    "Platform": "Job Platform",
                    "Interview Rate (%)": st.column_config.ProgressColumn(
                        "Interview Rate", format="%.1f%%", min_value=0, max_value=100
                    ),
                },
            )

        # ----- Timeline + titles -----
        t_left, t_right = st.columns(2, gap="medium")

        with t_left:
            with st.container(border=True):
                card_header("Your weekly pace", "Applications sent per week")
                dates = pd.to_datetime(apps_df["applied_date"], errors="coerce").dropna()
                if dates.empty:
                    st.info("No valid application dates yet.")
                else:
                    weekly = (
                        dates.dt.to_period("W").dt.start_time.value_counts()
                        .sort_index().rename_axis("Week").reset_index(name="Applications")
                    )
                    line = alt.Chart(weekly).encode(
                        x=alt.X("Week:T", title=None, axis=alt.Axis(format="%d %b")),
                        y=alt.Y("Applications:Q", title=None),
                        tooltip=[alt.Tooltip("Week:T", format="%d %b %Y"), "Applications"],
                    )
                    area = line.mark_area(
                        color=alt.Gradient(
                            gradient="linear",
                            stops=[alt.GradientStop(color="#6C5CE766", offset=0),
                                   alt.GradientStop(color="#6C5CE705", offset=1)],
                            x1=1, x2=1, y1=1, y2=0,
                        ),
                        interpolate="monotone",
                    )
                    stroke = line.mark_line(color=PURPLE, strokeWidth=3,
                                            interpolate="monotone")
                    dots = line.mark_point(color=PURPLE, fill="white", size=70,
                                           strokeWidth=2.5)
                    st.altair_chart(style_chart(area + stroke + dots, 280),
                                    width="stretch")

        with t_right:
            with st.container(border=True):
                card_header("Job titles that get interviews", "Top titles by interview invitations")
                if title_df.empty:
                    st.info("No interview history found yet.")
                else:
                    tbar = alt.Chart(title_df).mark_bar(
                        color=BLUE, cornerRadiusTopRight=8, cornerRadiusBottomRight=8, size=22
                    ).encode(
                        y=alt.Y("Job Title:N", sort="-x", title=None),
                        x=alt.X("Interviews:Q", title=None,
                                axis=alt.Axis(tickMinStep=1)),
                        tooltip=["Job Title", "Applications", "Interviews"],
                    )
                    st.altair_chart(style_chart(tbar, 280), width="stretch")

# ---------- TAB 2: ADD APPLICATION ----------
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

# ---------- TAB 3: SAVED APPLICATIONS ----------
with tab_list:
    try:
        df = load_applications()

        if df.empty:
            st.info(
                "🌱 Your application list is empty. "
                "Add your first opportunity in the Add Application tab."
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
                width="stretch",
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