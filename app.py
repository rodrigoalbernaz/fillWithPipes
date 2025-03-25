import streamlit as st
import pandas as pd
import io

st.title("Conversor de archivo TXT con Settlement info")

# Entradas del usuario
settlement_currency = st.text_input("Moneda de liquidación (Settlement Currency):", value="USD")
exchange_rate = st.number_input("Tasa de cambio (Settlement Exchange Rate):", value=1.0, format="%.4f")

uploaded_file = st.file_uploader("Subí tu archivo TXT delimitado por |", type="txt")

if uploaded_file and settlement_currency and exchange_rate:
    # Leer el archivo
    df = pd.read_csv(uploaded_file, delimiter='|')

    # Aplicar cambios
    df['Settlement_Currency'] = settlement_currency
    df['Settlement_Exchange_Rate'] = exchange_rate
    df['Settlement_Amount'] = (df['Amount'] / exchange_rate).round(4)

    # Mostrar tabla
    st.subheader("Vista previa del archivo actualizado")
    st.dataframe(df)

    # Preparar archivo para descarga
    output = io.StringIO()
    df.to_csv(output, sep='|', index=False)
    st.download_button(
        label="📥 Descargar archivo actualizado",
        data=output.getvalue(),
        file_name="archivo_actualizado.txt",
        mime="text/plain"
    )
