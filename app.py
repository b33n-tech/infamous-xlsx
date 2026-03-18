import streamlit as st
import pandas as pd
import io

st.set_page_config(
    page_title="CSV → XLSX",
    page_icon="📄",
    layout="centered"
)

st.title("Convertisseur CSV → XLSX (robuste)")

uploaded_file = st.file_uploader(
    "Upload un fichier CSV",
    type=["csv"]
)


def read_csv_robust(file):
    """
    Lecture CSV tolérante :
    - auto séparateur
    - auto encodage
    - tolérance colonnes irrégulières
    """

    encodings = ["utf-8", "latin-1", "cp1252"]

    for enc in encodings:
        try:
            file.seek(0)

            df = pd.read_csv(
                file,
                sep=None,          # auto detect separator
                engine="python",   # nécessaire pour sep=None
                encoding=enc,
                on_bad_lines="skip"  # ignore lignes cassées
            )

            return df

        except Exception:
            continue

    raise Exception("Impossible de lire ce CSV")


if uploaded_file:

    try:

        df = read_csv_robust(uploaded_file)

        st.success("CSV chargé")
        st.write("Aperçu :")
        st.dataframe(df)

        # conversion XLSX
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
