"""
Results section components for CodexSafe frontend
"""

import streamlit as st
import json
from typing import Dict, Any, List, Optional


def render_security_score(score: int, findings_summary: Dict[str, Any]) -> None:
    """Render security score display"""
    st.markdown("### 🔒 Security Score")
    
    # Color based on score
    if score >= 80:
        color = "#28a745"  # Green
        status = "✅ PASSED"
    elif score >= 60:
        color = "#ffc107"  # Yellow
        status = "⚠️ WARNING"
    else:
        color = "#dc3545"  # Red
        status = "❌ FAILED"
    
    # Score display
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.metric(
            label="Overall Security Score",
            value=f"{score}/100",
            delta=None
        )
    
    with col2:
        st.markdown(f"""
        <div style="padding: 10px; border-radius: 5px; background-color: {color}20; border-left: 4px solid {color};">
            <strong>{status}</strong>
        </div>
        """, unsafe_allow_html=True)
    
    # Findings summary
    if findings_summary:
        st.markdown("**Findings Summary:**")
        for severity, count in findings_summary.items():
            if count > 0:
                st.text(f"{severity.title()}: {count}")


def render_security_findings(findings: List[Dict[str, Any]]) -> None:
    """Render security findings"""
    if not findings:
        st.success("🎉 No security issues found!")
        return
    
    st.markdown("### 🔍 Security Findings")
    
    for i, finding in enumerate(findings):
        severity = finding.get("severity", "unknown").upper()
        
        # Color code by severity
        if severity == "CRITICAL":
            color = "#dc3545"
            icon = "🚨"
        elif severity == "HIGH":
            color = "#fd7e14"
            icon = "⚠️"
        elif severity == "MEDIUM":
            color = "#ffc107"
            icon = "🔸"
        else:
            color = "#6c757d"
            icon = "ℹ️"
        
        with st.expander(f"{icon} {finding.get('title', 'Security Issue')} - {severity}", expanded=severity in ["CRITICAL", "HIGH"]):
            st.markdown(f"**Issue:** {finding.get('description', 'No description available')}")
            
            if finding.get('file_path'):
                st.markdown(f"**File:** `{finding.get('file_path')}`")
            
            if finding.get('line_number'):
                st.markdown(f"**Line:** {finding.get('line_number')}")
            
            if finding.get('recommendation'):
                st.markdown(f"**Recommendation:** {finding.get('recommendation')}")
            
            if finding.get('code_snippet'):
                st.code(finding.get('code_snippet'), language='python')


def render_code_comparison(original_code: str, fixed_code: str) -> None:
    """Render code comparison between original and fixed versions"""
    st.markdown("### 📊 Code Comparison")
    
    if not fixed_code:
        st.info("No fixes were applied to the code.")
        return
    
    if original_code == fixed_code:
        st.success("✅ No changes needed - code was already secure!")
        return
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🔴 Original Code")
        st.code(original_code, language='python')
    
    with col2:
        st.markdown("#### 🟢 Fixed Code")
        st.code(fixed_code, language='python')
    
    # Show differences
    if st.checkbox("Show detailed differences"):
        st.markdown("#### 🔍 Changes Made")
        
        import difflib
        diff = difflib.unified_diff(
            original_code.splitlines(keepends=True),
            fixed_code.splitlines(keepends=True),
            fromfile='Original',
            tofile='Fixed',
            lineterm=''
        )
        
        diff_text = ''.join(diff)
        if diff_text:
            st.code(diff_text, language='diff')
        else:
            st.info("No differences detected")


def render_compliance_status(compliance_status: Dict[str, Any]) -> None:
    """Render compliance status"""
    st.markdown("### 📋 Compliance Status")
    
    if not compliance_status:
        st.info("No compliance information available.")
        return
    
    # OWASP Top 10
    if compliance_status.get("owasp"):
        st.markdown("#### 🛡️ OWASP Top 10")
        owasp_status = compliance_status["owasp"]
        
        for category, status in owasp_status.items():
            if status.get("compliant", False):
                st.success(f"✅ {category}: Compliant")
            else:
                st.error(f"❌ {category}: Non-compliant - {status.get('reason', 'Unknown issue')}")
    
    # Additional compliance standards
    standards = ["NIST", "SOC2", "HIPAA", "PCI_DSS"]
    for standard in standards:
        if compliance_status.get(standard.lower()):
            status = compliance_status[standard.lower()]
            if status.get("compliant", False):
                st.success(f"✅ {standard}: Compliant")
            else:
                st.warning(f"⚠️ {standard}: {status.get('status', 'Unknown')}")


def render_security_gate(passed: bool, reasons: List[str], score: int, critical_count: int, high_count: int) -> None:
    """Render security gate status"""
    st.markdown("### 🚪 Security Gate")
    
    if passed:
        st.success("🎉 **SECURITY GATE PASSED** - Code is ready for deployment!")
        st.balloons()
    else:
        st.error("🚫 **SECURITY GATE BLOCKED** - Code cannot be deployed")
    
    # Gate criteria
    col1, col2, col3 = st.columns(3)
    
    with col1:
        score_color = "green" if score >= 80 else "red"
        st.metric(
            label="Security Score",
            value=f"{score}/100",
            help="Must be ≥ 80 to pass"
        )
    
    with col2:
        critical_color = "green" if critical_count == 0 else "red"
        st.metric(
            label="Critical Issues",
            value=critical_count,
            help="Must be 0 to pass"
        )
    
    with col3:
        high_color = "green" if high_count == 0 else "red"
        st.metric(
            label="High Issues", 
            value=high_count,
            help="Must be 0 to pass"
        )
    
    # Reasons for gate decision
    if reasons:
        with st.expander("Gate Decision Details"):
            for reason in reasons:
                st.text(f"• {reason}")


def render_download_section(artifacts: List[Dict[str, Any]]) -> None:
    """Render download section for artifacts"""
    if not artifacts:
        st.info("No artifacts available for download.")
        return
    
    st.markdown("### 📥 Download Artifacts")
    
    for artifact in artifacts:
        artifact_name = artifact.get("name", "Unknown")
        artifact_description = artifact.get("description", "")
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.text(f"📄 {artifact_name}")
            if artifact_description:
                st.caption(artifact_description)
        
        with col2:
            try:
                with open(artifact.get("path", ""), "rb") as f:
                    file_data = f.read()
                
                st.download_button(
                    label="Download",
                    data=file_data,
                    file_name=artifact_name,
                    mime="application/octet-stream",
                    key=f"download_{artifact_name}"
                )
            except Exception as e:
                st.error(f"Error loading {artifact_name}: {str(e)}")


def render_results_summary(result: Dict[str, Any]) -> None:
    """Render overall results summary"""
    st.markdown("### 📊 Results Summary")
    
    summary_data = {
        "Pipeline Run ID": st.session_state.get("run_id", "Unknown"),
        "Processing Time": result.get("processing_time", "Unknown"),
        "Security Score": f"{result.get('final_score', 0)}/100",
        "Total Issues Found": len(result.get("security_review", {}).get("findings", [])),
        "Auto-Fix Attempts": result.get("autofix_attempts", 0),
        "Security Gate Passed": "Yes" if result.get("gate_passed", False) else "No"
    }
    
    for key, value in summary_data.items():
        col1, col2 = st.columns([1, 2])
        with col1:
            st.text(f"**{key}:**")
        with col2:
            st.text(str(value))
    
    # Additional insights
    if result.get("insights"):
        st.markdown("#### 💡 Insights")
        for insight in result.get("insights", []):
            st.text(f"• {insight}")
