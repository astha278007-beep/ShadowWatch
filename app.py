import streamlit as st
import pandas as pd

from backend.tamper_detector import detect_tampering
from backend.evidence_blockchain import (
    create_evidence_record,
    verify_blockchain,
    verify_evidence_integrity,
    simulate_blockchain_tampering,
    reset_blockchain
)
from backend.database import (
    initialize_database,
    save_incident,
    get_incidents
)

# --------------------------------
# PAGE CONFIGURATION
# --------------------------------
st.set_page_config(
    page_title="ShadowWatch",
    page_icon="🛡️",
    layout="wide"
)

# Initialize database
initialize_database()

# --------------------------------
# VIDEO SELECTION
# --------------------------------
video_option = st.selectbox(
    "Select CCTV Feed for Analysis",
    ["Normal CCTV Feed", "Tampered CCTV Feed"]
)

if video_option == "Normal CCTV Feed":
    VIDEO_PATH = "videos/primary_cctv.mp4"
else:
    VIDEO_PATH = "videos/tampered_cctv.mp4"


# --------------------------------
# SESSION STATE
# --------------------------------
if "tampering_detected" not in st.session_state:
    st.session_state.tampering_detected = False

if "reason" not in st.session_state:
    st.session_state.reason = "System monitoring active"

if "evidence_record" not in st.session_state:
    st.session_state.evidence_record = None

if "incident_saved" not in st.session_state:
    st.session_state.incident_saved = False


# --------------------------------
# TITLE
# --------------------------------
st.title("🛡️ ShadowWatch")
st.subheader(
    "Intelligent CCTV Tampering Detection & Evidence Protection System"
)

st.caption(
    "Real-time surveillance monitoring • Tampering detection • "
    "Secure evidence protection • Blockchain integrity verification"
)

st.divider()


# --------------------------------
# STATUS SECTION
# --------------------------------
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Primary Camera",
        "OFFLINE 🔴" if st.session_state.tampering_detected else "ONLINE 🟢"
    )

with col2:
    st.metric(
        "Threat Status",
        "TAMPERING 🚨" if st.session_state.tampering_detected else "NORMAL"
    )

with col3:
    st.metric(
        "Backup Source",
        "ACTIVE 🟢" if st.session_state.tampering_detected else "STANDBY"
    )

with col4:
    st.metric(
        "Blockchain",
        "VERIFIED ⛓️" if verify_blockchain() else "COMPROMISED ❌"
    )

if st.session_state.tampering_detected:
    st.error("🚨 SYSTEM ALERT: CCTV tampering incident is currently active.")
else:
    st.success("🟢 SYSTEM STATUS: All surveillance components are operating normally.")

st.divider()


# --------------------------------
# MAIN LAYOUT
# --------------------------------
left, right = st.columns([2, 1])

with left:
    st.subheader("📹 Primary CCTV Feed")
    st.caption(f"Currently analyzing: {video_option}")
    st.video(VIDEO_PATH)


with right:
    st.subheader("🛡️ Security Controls")
    st.caption("Run surveillance analysis or test the security response system.")

    if st.button(
        "🔍 RUN TAMPERING DETECTION",
        use_container_width=True
    ):

        with st.spinner("Analyzing CCTV feed..."):
            result = detect_tampering(VIDEO_PATH)

        if result["tampering_detected"]:

            st.session_state.tampering_detected = True
            st.session_state.reason = result["reason"]

            # Create evidence record
            if st.session_state.evidence_record is None:

                evidence_record = create_evidence_record(
                    VIDEO_PATH,
                    result["reason"]
                )

                st.session_state.evidence_record = evidence_record

            # Save incident only once
            if not st.session_state.incident_saved:

                save_incident(
                    result["reason"],
                    VIDEO_PATH,
                    st.session_state.evidence_record["evidence_hash"]
                )

                st.session_state.incident_saved = True

            st.error("🚨 TAMPERING DETECTED!")
            st.warning(result["reason"])
            st.success("🤫 Silent Security Mode Activated")
            st.success("🎥 Backup Evidence Source Activated")
            st.success("💾 Incident securely saved to database")

        else:
            st.session_state.tampering_detected = False
            st.session_state.reason = result["reason"]

            st.success("✅ NO TAMPERING DETECTED")
            st.info(result["reason"])


    if st.button(
        "🔄 RESET SYSTEM",
        use_container_width=True
    ):
        st.session_state.tampering_detected = False
        st.session_state.reason = "System monitoring active"
        st.session_state.evidence_record = None
        st.session_state.incident_saved = False    
        reset_blockchain()

        st.rerun()


    # --------------------------------
    # BLOCKCHAIN TAMPERING SIMULATION
    # --------------------------------
    if st.button(
        "🧪 SIMULATE BLOCKCHAIN TAMPERING",
        use_container_width=True
    ):

        if simulate_blockchain_tampering():
            st.warning("⚠️ Blockchain tampering simulation activated!")
            st.rerun()
        else:
            st.info("No blockchain record available to tamper with.")


st.divider()


# --------------------------------
# SECURITY EVENT STATUS
# --------------------------------
st.subheader("📋 Security Event Status")

if st.session_state.tampering_detected:
    st.error(
        f"ACTIVE INCIDENT: {st.session_state.reason}"
    )
else:
    st.success(
        "No active incidents. CCTV monitoring is active."
    )


st.divider()


# --------------------------------
# EVIDENCE BLOCKCHAIN
# --------------------------------
st.subheader("⛓️ Evidence Blockchain")
st.caption(
    "Cryptographically secured evidence records with blockchain-style "
    "integrity verification."
)

if st.session_state.evidence_record:

    record = st.session_state.evidence_record

    st.success("✓ Evidence securely recorded on blockchain")

    st.write("**Block Number:**", record["index"])
    st.write("**Timestamp:**", record["timestamp"])

    st.write("**Evidence SHA-256 Hash:**")
    st.code(record["evidence_hash"])

    st.write("**Previous Block Hash:**")
    st.code(record["previous_hash"])

    st.write("**Current Block Hash:**")
    st.code(record["block_hash"])

    # --------------------------------
    # EVIDENCE INTEGRITY VERIFICATION
    # --------------------------------
    if st.button(
        "🔐 VERIFY EVIDENCE INTEGRITY",
        use_container_width=True
    ):

        verification = verify_evidence_integrity(
            record["evidence_file"],
            record["evidence_hash"]
        )

        if verification["integrity_verified"]:
            st.success("✅ EVIDENCE INTEGRITY VERIFIED")
            st.info(
                "The current evidence hash matches the original hash. "
                "No modification detected."
            )
        else:
            st.error("🚨 EVIDENCE MODIFIED!")
            st.warning(
                "The current evidence hash does not match the original hash."
            )

        st.write("**Original Hash:**")
        st.code(verification["original_hash"])

        st.write("**Current Hash:**")
        st.code(verification["current_hash"])

else:
    st.success("✓ Blockchain integrity: VERIFIED")


st.divider()


# --------------------------------
# SECURE BACKUP EVIDENCE
# --------------------------------
st.subheader("🎥 Secure Backup Evidence")

st.caption(
    "A protected backup source is automatically activated when CCTV tampering is detected."
)

if st.session_state.tampering_detected:
    st.success("Backup evidence source activated successfully")
    st.caption("Original CCTV evidence preserved securely.")
    st.video("videos/primary_cctv.mp4")
else:
    st.info("Backup evidence will activate automatically if tampering is detected.")

st.divider()


# --------------------------------
# INCIDENT HISTORY
# --------------------------------
st.subheader("📋 Incident History")

st.caption(
    "Chronological record of detected security incidents. "
    "Most recent incidents are displayed first."
)

incidents = get_incidents()

if incidents:
    df = pd.DataFrame(
        incidents,
        columns=[
            "Incident ID",
            "Timestamp",
            "Reason",
            "Evidence File",
            "Status"
        ]
    )

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

else:
    st.info("No incidents recorded yet.")