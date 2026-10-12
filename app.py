
import sqlite3
from datetime import datetime

import pandas as pd
import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

DB_NAME = "lost_found.db"

st.set_page_config(
    page_title="AI Lost & Found Agent",
    page_icon="🔎",
    layout="wide"
)


# ---------------- DATABASE ----------------

def get_connection():
    return sqlite3.connect(DB_NAME)


def initialize_database():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                report_type TEXT NOT NULL,
                item_name TEXT NOT NULL,
                category TEXT NOT NULL,
                color TEXT,
                location TEXT NOT NULL,
                description TEXT NOT NULL,
                contact TEXT NOT NULL,
                created_at TEXT NOT NULL,
                status TEXT DEFAULT 'Open'
            )
        """)


def add_report(report):
    with get_connection() as conn:
        conn.execute("""
            INSERT INTO reports (
                report_type, item_name, category, color,
                location, description, contact, created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, report)


def load_reports():
    with get_connection() as conn:
        return pd.read_sql_query(
            "SELECT * FROM reports ORDER BY id DESC",
            conn
        )


# ---------------- AI MATCHING ----------------

def item_text(row):
    return " ".join([
        str(row.get("item_name", "")),
        str(row.get("category", "")),
        str(row.get("color", "")),
        str(row.get("location", "")),
        str(row.get("description", ""))
    ]).lower()


def find_matches(report_id, reports):
    current = reports[reports["id"] == report_id]

    if current.empty:
        return []

    item = current.iloc[0]

    opposite_type = (
        "Found" if item["report_type"] == "Lost"
        else "Lost"
    )

    candidates = reports[
        (reports["report_type"] == opposite_type)
        & (reports["status"] == "Open")
        & (reports["id"] != report_id)
    ].copy()

    if candidates.empty:
        return []

    documents = [item_text(item)] + [
        item_text(row)
        for _, row in candidates.iterrows()
    ]

    vectorizer = TfidfVectorizer(
        ngram_range=(1, 2),
        stop_words="english"
    )

    matrix = vectorizer.fit_transform(documents)
    scores = cosine_similarity(
        matrix[0:1], matrix[1:]
    )[0]

    candidates["match_score"] = scores * 100

    # Small boost for exact category and location agreement.
    for index, candidate in candidates.iterrows():
        boost = 0

        if str(item["category"]).lower() == str(
            candidate["category"]
        ).lower():
            boost += 8

        if str(item["location"]).lower() == str(
            candidate["location"]
        ).lower():
            boost += 8

        candidates.loc[index, "match_score"] = min(
            100,
            candidates.loc[index, "match_score"] + boost
        )

    candidates = candidates.sort_values(
        "match_score", ascending=False
    )

    return candidates.to_dict("records")


# ---------------- APPLICATION ----------------

initialize_database()

st.title("🔎 AI-Powered Digital Lost & Found Agent")
st.caption(
    "Report missing items and discover possible matches "
    "using AI-powered text similarity."
)

dashboard, report_tab, matches_tab, all_tab = st.tabs([
    "Dashboard",
    "Submit Report",
    "Find Matches",
    "All Reports"
])

reports = load_reports()

with dashboard:
    total = len(reports)
    lost_count = (
        int((reports["report_type"] == "Lost").sum())
        if total else 0
    )
    found_count = (
        int((reports["report_type"] == "Found").sum())
        if total else 0
    )

    c1, c2, c3 = st.columns(3)
    c1.metric("Total Reports", total)
    c2.metric("Lost Items", lost_count)
    c3.metric("Found Items", found_count)

    st.subheader("Recent Reports")

    if total:
        st.dataframe(
            reports[
                ["id", "report_type", "item_name",
                 "category", "location", "status"]
            ],
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No reports yet. Submit your first report!")

with report_tab:
    st.subheader("Report a Lost or Found Item")

    with st.form("report_form"):
        report_type = st.radio(
            "Report type",
            ["Lost", "Found"],
            horizontal=True
        )

        item_name = st.text_input(
            "Item name",
            placeholder="e.g. Black leather wallet"
        )

        category = st.selectbox(
            "Category",
            [
                "Wallet", "Phone", "Keys", "Bag",
                "ID Card", "Electronics", "Books",
                "Clothing", "Jewellery", "Other"
            ]
        )

        color = st.text_input(
            "Item color",
            placeholder="e.g. Black"
        )

        location = st.text_input(
            "Location",
            placeholder="e.g. College library"
        )

        description = st.text_area(
            "Description",
            placeholder=(
                "Describe the item, when it was lost "
                "or found, and other identifying details."
            )
        )

        contact = st.text_input(
            "Contact information",
            placeholder="Email or another safe contact method"
        )

        submitted = st.form_submit_button(
            "Submit Report",
            type="primary"
        )

        if submitted:
            if not all([
                item_name.strip(),
                location.strip(),
                description.strip(),
                contact.strip()
            ]):
                st.error(
                    "Please fill in the item name, location, "
                    "description and contact information."
                )
            else:
                add_report((
                    report_type,
                    item_name.strip(),
                    category,
                    color.strip(),
                    location.strip(),
                    description.strip(),
                    contact.strip(),
                    datetime.now().isoformat(timespec="seconds")
                ))

                st.success("Report submitted successfully!")
                st.rerun()

with matches_tab:
    st.subheader("Find Possible Matches")

    reports = load_reports()

    if reports.empty:
        st.info("Submit a report first.")
    else:
        report_options = {
            f"#{row['id']} - {row['report_type']}: "
            f"{row['item_name']}": int(row["id"])
            for _, row in reports.iterrows()
        }

        selected = st.selectbox(
            "Select a report",
            list(report_options.keys())
        )

        if st.button("Find AI Matches", type="primary"):
            results = find_matches(
                report_options[selected],
                reports
            )

            if not results:
                st.warning(
                    "No possible matches found yet. "
                    "Try again when more reports are submitted."
                )
            else:
                st.write(
                    "Results are ranked by description similarity. "
                    "A high score is not proof of ownership."
                )

                for result in results:
                    score = result["match_score"]

                    with st.container(border=True):
                        st.subheader(
                            f"{result['item_name']} "
                            f"({score:.1f}% match score)"
                        )

                        st.write(
                            f"**Type:** {result['report_type']}"
                        )
                        st.write(
                            f"**Category:** {result['category']}"
                        )
                        st.write(f"**Color:** {result['color']}")
                        st.write(
                            f"**Location:** {result['location']}"
                        )
                        st.write(
                            f"**Description:** "
                            f"{result['description']}"
                        )

                        st.caption(
                            "Contact details are hidden in this "
                            "prototype. Verify ownership before "
                            "arranging a handover."
                        )

with all_tab:
    st.subheader("All Lost & Found Reports")

    reports = load_reports()

    if reports.empty:
        st.info("No reports available.")
    else:
        st.dataframe(
            reports[
                ["id", "report_type", "item_name", "category",
                 "color", "location", "description",
                 "created_at", "status"]
            ],
            use_container_width=True,
            hide_index=True
        )

st.divider()
st.caption(
    "Student project prototype | AI-assisted matching "
    "| Always verify ownership before returning an item."
)