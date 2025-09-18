import streamlit as st

def filters(df):
    st.markdown('<div class="sticky-header">', unsafe_allow_html=True)

    cols = st.columns([2, 4, 4])
    with cols[0]:
        st.markdown("### 🔍 Filters")

    # City filter
    with cols[1]:
        all_cities = df["City"].dropna().unique()
        selected_city = st.selectbox("Select City", options=all_cities, index=0)

    # Technology filter (multiselect)
    with cols[2]:
        all_tech = df["Technology"].dropna().unique()
        selected_tech = st.multiselect(
            "Select Technology",
            options=all_tech,
            default=["4G"] if "4G" in all_tech else all_tech[0]
        )

    st.markdown('</div>', unsafe_allow_html=True)

    # Apply filters
    filtered_df = df[(df["City"] == selected_city) & (df["Technology"].isin(selected_tech))]
    return filtered_df
