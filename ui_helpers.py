import streamlit as st


def render_header(title: str, subtitle: str | None = None) -> None:
    """Render a styled header block."""
    subtitle_html = f"<div style='color:#6b7280;font-size:14px'>{subtitle}</div>" if subtitle else ""
    st.markdown(
        f"""
        <div style="display:flex;align-items:center;justify-content:space-between;background:linear-gradient(90deg,#f6fbff,#eef6ff);border-radius:10px;padding:12px 18px;margin-bottom:12px;box-shadow:0 2px 6px rgba(16,24,40,0.04);">
          <div style="display:flex;flex-direction:column;">
            <div style="font-size:36px;font-weight:700;color:#0b3d91;">{title}</div>
            {subtitle_html}
          </div>
          <div style="font-size:20px;color:#9aa4b2;">&nbsp;</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_kpi_row(metrics: list[dict]) -> None:
    """Render KPI cards from a list of metric dicts.

    Each metric dict should contain: {label, value, delta (optional), color (optional)}
    """
    if not metrics:
        return
    cols = st.columns(len(metrics), gap="large")
    for c, m in zip(cols, metrics):
        label = m.get('label', '')
        value = m.get('value', '—')
        delta = m.get('delta')
        color = m.get('color', '#0b3d91')
        html = f"""
        <div style='background:white;border-radius:10px;padding:12px;box-shadow:0 1px 4px rgba(2,6,23,0.06);'>
          <div style='font-size:12px;color:#6b7280;margin-bottom:6px;'>{label}</div>
          <div style='font-size:22px;font-weight:700;color:{color};'>{value}</div>
          {f"<div style='font-size:12px;color:#10B981;margin-top:6px;'>{delta}</div>" if delta else ''}
        </div>
        """
        c.markdown(html, unsafe_allow_html=True)
