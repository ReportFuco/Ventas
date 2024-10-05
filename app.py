import streamlit as st
import extraccion_venta as ev


class PagVentasIdeal:
    """Configuración del sitio web a través de Python y Streamlit"""

    def __init__(self, ) -> None:
        st.set_page_config("DashBoard Ideal", "img/Logo IDEAL OSITO RGB.png")
    

    def tabla_ventas(self):

        df = ev.VentaIdeal().extractor_data()
        st.text("Descargando, dale tiempo inpaciente")
        st.dataframe(df)

if __name__=="__main__":

    PagVentasIdeal().tabla_ventas()