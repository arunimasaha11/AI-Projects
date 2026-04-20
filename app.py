import streamlit as st
import time
from pipeline import run_research_pipeline

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Research System",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; }

html, body, [data-testid="stAppViewContainer"] {
    background: #0a0a0f;
    color: #343434;
    font-family: 'DM Mono', monospace;
}

[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(ellipse 80% 50% at 20% 10%, rgba(99,60,180,0.18) 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 80% 80%, rgba(34,197,180,0.12) 0%, transparent 55%),
        #0a0a0f;
}

/* Hide default streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stToolbar"] { display: none; }

/* ── Hero header ── */
.hero {
    text-align: center;
    padding: 3.5rem 1rem 2rem;
    position: relative;
}
.hero-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.72rem;
    font-weight: 500;
    letter-spacing: 0.25em;
    color: #22c5b4;
    text-transform: uppercase;
    margin-bottom: 0.75rem;
}
.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: clamp(2.4rem, 5vw, 4rem);
    font-weight: 800;
    line-height: 1.05;
    background: linear-gradient(135deg, #ffffff 0%, #c8b8ff 50%, #22c5b4 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0 0 1rem;
}
.hero-sub {
    font-size: 0.88rem;
    color: #8a8aab;
    letter-spacing: 0.04em;
    max-width: 480px;
    margin: 0 auto;
    line-height: 1.7;
}

/* ── Input card ── */
.input-card {
    background: rgba(255,255,255,0.035);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px;
    padding: 2rem 2.2rem;
    max-width: 720px;
    margin: 0 auto 2.5rem;
    backdrop-filter: blur(12px);
}

/* Streamlit text input override */
[data-testid="stTextInput"] input {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    border-radius: 10px !important;
    color: #343434 !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.95rem !important;
    padding: 0.75rem 1rem !important;
    transition: border-color 0.2s;
}
[data-testid="stTextInput"] input:focus {
    border-color: #7c4dff !important;
    box-shadow: 0 0 0 3px rgba(124,77,255,0.15) !important;
}
[data-testid="stTextInput"] label {
    color: #343434 !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.78rem !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
}

/* Streamlit button override */
[data-testid="stButton"] > button {
    background: linear-gradient(135deg, #7c4dff, #22c5b4) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    letter-spacing: 0.06em !important;
    padding: 0.65rem 2.2rem !important;
    cursor: pointer !important;
    transition: opacity 0.2s, transform 0.15s !important;
    width: 100% !important;
}
[data-testid="stButton"] > button:hover {
    opacity: 0.88 !important;
    transform: translateY(-1px) !important;
}

/* ── Pipeline step cards ── */
.step-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 12px;
    padding: 1.4rem 1.6rem;
    margin-bottom: 1.2rem;
    position: relative;
    overflow: hidden;
}
.step-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 3px; height: 100%;
    background: linear-gradient(180deg, #7c4dff, #22c5b4);
    border-radius: 3px 0 0 3px;
}
.step-header {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin-bottom: 0.85rem;
}
.step-badge {
    font-family: 'DM Mono', monospace;
    font-size: 0.68rem;
    font-weight: 500;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    background: rgba(124,77,255,0.2);
    color: #b49aff;
    border: 1px solid rgba(124,77,255,0.3);
    border-radius: 6px;
    padding: 0.2rem 0.6rem;
}
.step-title {
    font-family: 'Syne', sans-serif;
    font-size: 1rem;
    font-weight: 700;
    color: #e0ddf5;
}
.step-content {
    font-size: 0.82rem;
    color: #9a97b8;
    line-height: 1.75;
    white-space: pre-wrap;
    word-break: break-word;
    max-height: 320px;
    overflow-y: auto;
    padding-right: 0.5rem;
}
.step-content::-webkit-scrollbar { width: 4px; }
.step-content::-webkit-scrollbar-track { background: transparent; }
.step-content::-webkit-scrollbar-thumb { background: rgba(124,77,255,0.4); border-radius: 4px; }

/* ── Final report card ── */
.report-card {
    background: rgba(124,77,255,0.07);
    border: 1px solid rgba(124,77,255,0.25);
    border-radius: 16px;
    padding: 2rem 2.2rem;
    margin-top: 1rem;
}
.report-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.3rem;
    font-weight: 800;
    color: #c8b8ff;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 0.6rem;
}
.report-body {
    font-size: 0.88rem;
    color: #ccc9e8;
    line-height: 1.85;
    white-space: pre-wrap;
    word-break: break-word;
}

/* ── Feedback card ── */
.feedback-card {
    background: rgba(34,197,180,0.06);
    border: 1px solid rgba(34,197,180,0.2);
    border-radius: 16px;
    padding: 1.8rem 2.2rem;
    margin-top: 1.2rem;
}
.feedback-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.1rem;
    font-weight: 700;
    color: #22c5b4;
    margin-bottom: 0.85rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.feedback-body {
    font-size: 0.85rem;
    color: #a0d8d3;
    line-height: 1.8;
    white-space: pre-wrap;
    word-break: break-word;
}

/* ── Status pill ── */
.status-running {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    background: rgba(124,77,255,0.15);
    border: 1px solid rgba(124,77,255,0.3);
    border-radius: 999px;
    padding: 0.3rem 1rem;
    font-size: 0.75rem;
    color: #b49aff;
    letter-spacing: 0.08em;
    font-family: 'DM Mono', monospace;
    margin-bottom: 1.5rem;
}
.pulse {
    width: 7px; height: 7px;
    background: #7c4dff;
    border-radius: 50%;
    animation: pulse 1.2s ease-in-out infinite;
}
@keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50%       { opacity: 0.4; transform: scale(0.7); }
}

/* ── Divider ── */
.divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.08), transparent);
    margin: 2rem 0;
}
</style>
""", unsafe_allow_html=True)


# ── Hero ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-label">✦ Multi-Agent System</div>
    <h1 class="hero-title">AI Research Pipeline</h1>
    <p class="hero-sub">Enter any topic. Four specialized agents — Search, Reader, Writer & Critic — collaborate to produce a verified research report.</p>
</div>
""", unsafe_allow_html=True)


# ── Input card ─────────────────────────────────────────────────────────────────
st.markdown('<div class="input-card">', unsafe_allow_html=True)
topic = st.text_input("Research Topic", placeholder="e.g. Latest advancements in Quantum Computing")
run = st.button("🚀  Launch Research Pipeline")
st.markdown('</div>', unsafe_allow_html=True)


# ── Pipeline execution ─────────────────────────────────────────────────────────
if run:
    if not topic.strip():
        st.warning("Please enter a research topic first.")
    else:
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="status-running">
            <div class="pulse"></div> Pipeline running — {topic}
        </div>
        """, unsafe_allow_html=True)

        # Placeholders for live step updates
        ph_search   = st.empty()
        ph_reader   = st.empty()
        ph_writer   = st.empty()
        ph_critic   = st.empty()
        ph_report   = st.empty()
        ph_feedback = st.empty()

        def render_step(placeholder, badge, title, content, done=False):
            accent = "✦" if done else "⟳"
            placeholder.markdown(f"""
            <div class="step-card">
                <div class="step-header">
                    <span class="step-badge">{badge}</span>
                    <span class="step-title">{accent} {title}</span>
                </div>
                <div class="step-content">{content}</div>
            </div>
            """, unsafe_allow_html=True)

        # Step 1 — Search Agent
        render_step(ph_search, "Step 01", "Search Agent", "Searching for reliable information...")

        with st.spinner(""):
            try:
                from agents import build_search_agent
                search_agent = build_search_agent()
                search_result = search_agent.invoke({
                    "messages": [("user", f"Find recent, reliable and detailed information about: {topic}")]
                })
                search_content = search_result['messages'][-1].content
                render_step(ph_search, "Step 01", "Search Agent", search_content[:1200], done=True)

                # Step 2 — Reader Agent
                render_step(ph_reader, "Step 02", "Reader Agent", "Scraping top resources...")
                from agents import build_reader_agent
                reader_agent = build_reader_agent()
                reader_result = reader_agent.invoke({
                    "messages": [("user",
                        f"Based on the following search results about '{topic}', "
                        f"pick the most relevant URL and scrape it for deeper content.\n\n"
                        f"Search Results:\n{search_content[:800]}"
                    )]
                })
                scraped_content = reader_result['messages'][-1].content
                render_step(ph_reader, "Step 02", "Reader Agent", scraped_content[:1200], done=True)

                # Step 3 — Writer Agent
                render_step(ph_writer, "Step 03", "Writer Agent", "Drafting the research report...")
                from agents import writer_chain
                research_combined = (
                    f"Search Results:\n{search_content}\n\n"
                    f"Detailed Scraped Content:\n{scraped_content}"
                )
                report = writer_chain.invoke({"topic": topic, "research": research_combined})
                render_step(ph_writer, "Step 03", "Writer Agent", "Report drafted successfully ✦", done=True)

                # Step 4 — Critic Agent
                render_step(ph_critic, "Step 04", "Critic Agent", "Reviewing the report...")
                from agents import critic_chain
                feedback = critic_chain.invoke({"report": report})
                render_step(ph_critic, "Step 04", "Critic Agent", "Review complete ✦", done=True)

                # ── Final Report ──
                st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
                ph_report.markdown(f"""
                <div class="report-card">
                    <div class="report-title">📄 Final Research Report</div>
                    <div class="report-body">{report}</div>
                </div>
                """, unsafe_allow_html=True)

                # ── Critic Feedback ──
                ph_feedback.markdown(f"""
                <div class="feedback-card">
                    <div class="feedback-title">🔍 Critic Feedback</div>
                    <div class="feedback-body">{feedback}</div>
                </div>
                """, unsafe_allow_html=True)

            except Exception as e:
                st.error(f"Pipeline error: {e}")