import streamlit as st

def subject_card(name, code, section, stats=None, footer_callback=None):
    html = f"""
    <div style="
        background:#FFFFFF;
        border-left:8px solid #EB459E;
        border:1px solid #000000;
        border-radius:20px;
        padding:25px;
        margin-bottom:20px;
    ">

        <h3 style="
            margin:0;
            color:#111111;
            font-size:1.5rem;
            font-weight:700;
        ">
            {name}
        </h3>

        <p style="
            color:#111111;
            margin:10px 0 18px 0;
            font-size:1rem;
        ">
            Code :
            <span style="
                background:#E0E3FF;
                color:#5865F2;
                padding:2px 8px;
                border-radius:6px;
                font-weight:600;
            ">
                {code}
            </span>

            &nbsp; | &nbsp;

            Section :
            <span style="color:#111111;font-weight:600;">
                {section}
            </span>
        </p>
    """

    if stats:
        html += """
        <div style="
            display:flex;
            gap:12px;
            flex-wrap:wrap;
        ">
        """

        for icon, label, value in stats:
            html += f"""
            <div style="
                background:#F8F1FF;
                color:#111111;
                padding:8px 14px;
                border-radius:12px;
                font-size:0.95rem;
                border:1px solid #E5E7EB;
            ">
                {icon}
                <b style="color:#111111;"> {value}</b>
                <span style="color:#111111;"> {label}</span>
            </div>
            """

        html += "</div>"

    html += "</div>"

    st.markdown(html, unsafe_allow_html=True)

    if footer_callback:
        footer_callback()