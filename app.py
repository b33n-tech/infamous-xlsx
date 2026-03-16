import streamlit as st
import pandas as pd
import io

st.set_page_config(
    page_title="CSV → XLSX",
    page_icon="📄",
    layout="centered"
)

st.title("Convertisseur CSV → XLSX")

uploaded_file = st.file_uploader(
    "Upload un fichier CSV",
    type=["csv"]
)

if uploaded_file:

    try:
        # Lire CSV
        df = pd.read_csv(uploaded_file)

        st.success("CSV chargé")
        st.write("Aperçu :")
        st.dataframe(df)

        # Convertir en XLSX en mémoire
        output = io.BytesIO()

        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            df.to_excel(writer, index=False, sheet_name="Sheet1")

        output.seek(0)

        st.download_button(
            label="Télécharger en XLSX",
            data=output,
            file_name="converti.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    except Exception as e:
        st.error(str(e))
