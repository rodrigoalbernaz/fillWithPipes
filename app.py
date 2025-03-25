import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="Conversor de archivo TXT", layout="centered")
st.title("📄 Conversor de archivo TXT con Settlement Info")

st.markdown("""
Este conversor permite cargar un archivo `.txt` delimitado por `|`, completar los campos
**Settlement_Currency** y **Settlement_Exchange_Rate**, y generar automáticamente la columna
**Settlement_Amount** con el cálculo correspondiente.
""")

# Entradas del usuario
settlement_currency = st.text_input("💱 Moneda de liquidación (Settlement Currency):", value="USD")
exchange_rate = st.number_input("💹 Tasa de cambio (Settlement Exchange Rate):", value=1.0, format="%.4f")

uploaded_file = st.file_uploader("📤 Subí tu archivo `.txt` delimitado por `|`", type="txt")

if uploaded_file and settlement_currency and exchange_rate:
    try:
        # Leer archivo
        df = pd.read_csv(uploaded_file, delimiter='|')

        # Validar que la columna Amount exista
        if 'Amount' not in df.columns:
            st.error("❌ La columna 'Amount' no está presente en el archivo.")
        else:
            # Agregar columnas
            df['Settlement_Currency'] = settlement_currency
            df['Settlement_Exchange_Rate'] = exchange_rate
            df['Settlement_Amount'] = (df['Amount'] * exchange_rate).round(4)

            # Mostrar preview
            st.subheader("👁️ Vista previa del archivo actualizado")
            st.dataframe(df)

            # Exportar como texto plano delimitado por |
            output = io.StringIO()
            txt_data = df.to_csv(sep='|', index=False, lineterminator='\n')
            output.write(txt_data)

            st.download_button(
                label="📥 Descargar archivo actualizado (.txt)",
                data=output.getvalue(),
                file_name="archivo_actualizado.txt",
                mime="text/plain"
            )
    except Exception as e:
        st.error(f"❌ Error al procesar el archivo: {e}")
